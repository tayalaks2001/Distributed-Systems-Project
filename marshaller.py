import struct
from messages.marshalable import Marshalable
from messages.balance_msg import *
from messages.dw_msg import *
from messages.create_new_account_output import * 
from messages.create_new_account_input import *
from enum import Enum
from bank_account import BankAccount
from unmarshaller import *

class Marshaller:
	
	@staticmethod
	def marshal_string(data: str):
		"""
		Marshal string using the string encode method.
		Keyword arguments:
		data: string to be marshalled

		Returns: 
		Marshalled string output/type error if data is not a string object.
		"""

		if not isinstance(data, str):
			print("Error! marshal_string called on non-string value!")
			raise TypeError

		result = bytes()

		str_len = len(data)
		str_len = Marshaller.marshal_int(str_len, 4)
		content = data.encode('utf-8')

		result += str_len + content

		return result


	@staticmethod
	def marshal_int(data: int, num_bytes: int = 8):
		"""
		Marshal int using the struct pack method.
		Keyword arguments:
		data: value to be marshalled
		num_bytes: number of bytes in output (4 or 8)

		Returns: 
		Marshalled int output/type error if data is not an int/float object.
		"""
		
		if isinstance(data, float):
			print("marshal_int called on float value! Converting to int...")
			data = int(data)
		
		if not isinstance(data, int):
			print("Error! marshal_int called on non-int value!")
			raise TypeError

		if num_bytes == 4:
			return struct.pack('<i', data)

		return struct.pack('<Q', data)

	
	@staticmethod
	def marshal_float(data):
		"""
		Marshal float using the struct pack method.
		Keyword arguments:
		data: value to be marshalled

		Returns: 
		Marshalled float output/type error if data is not an int/float object.
		"""

		if isinstance(data, int):
			print("marshal_float on int value! Converting to float...")
			data = float(data)

		if not isinstance(data, float):
			print("Error! marshal_float called on non-float value!")
			raise TypeError
			
		return struct.pack('<d', data)
	

	@staticmethod
	def marshal_enum(data):
		""""
		Marshal enum type object.
		Keyword arguments:
		data: value to be marshalled

		Returns: 
		Marshalled enum output/type error if data is not an enum object.
		"""

		if not isinstance(data, Enum):
			print("Error! marshal_enum called on non-enum value!")
			raise TypeError
		
		result = bytes()

		obj_type = type(data).object_type()
		result += Marshaller.marshal_int(obj_type, 4)
		result += Marshaller.marshal_int(data.value, 4)

		return result
	

	@staticmethod
	def marshal_object(data):
		"""
		Marshal objects derived from Marshalable class.
		Keyword arguments:
		data: object to be marshalled

		Returns: 
		Marshalled object output/type error if object doesn't have Marshalable as parent class.
		"""

		data_class = type(data)

		if not issubclass(data_class, Marshalable):
			print("Error! marshal_object called on non-marshalable object!")
			raise TypeError

		result = bytes()
		
		obj_type = data_class.object_type()
		result += Marshaller.marshal_int(obj_type, 4)

		fields_dict = data.get_fields()
		fields_type_dict = data_class.get_field_types()

		for field_id, field_val in fields_dict.items():
			field_type = fields_type_dict[field_id]
			result += Marshaller.marshal_int(field_id, 4)

			if field_type == int:
				result += Marshaller.marshal_int(field_val)
			elif field_type == float:
				result += Marshaller.marshal_float(field_val)
			elif field_type == str:
				result += Marshaller.marshal_string(field_val)
			elif field_type == Enum:
				result += Marshaller.marshal_enum(field_val)

		return result


def compile_message(message_id: int, object: Marshalable) -> bytes:
	"""
	Compile final message to be sent over.
	Keyword arguments:
	message_id: id from the response object being sent to client
	object: response object to be marshalled

	Returns: 
	Marshalled object output/type error if object doesn't have Marshalable as parent class.
	"""

	if not issubclass(type(object), Marshalable):
		print("Object sent to marshaller is inherited from Marshalable!")
		raise TypeError

	result = bytes()
	
	marshalled_message_id = Marshaller.marshal_int(message_id, 4)
	marshalled_object = Marshaller.marshal_object(object)

	result += marshalled_message_id + marshalled_object

	message_len = len(result)
	marshalled_message_len = Marshaller.marshal_int(message_len, 4)
	
	result = marshalled_message_len + result

	return result
