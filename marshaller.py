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
	def marshal_string(data):

		if not isinstance(data, str):
			print("Error! marshal_string called on non-string value!")
			raise TypeError

		result = bytes()

		str_len = len(data)
		str_len = Marshaller.marshal_int(str_len, 4)
		content = data.encode('utf-8')	# No format specifier available to marshal string in struct 

		result += str_len + content

		return result


	@staticmethod
	def marshal_int(data, num_bytes = 8):
		
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

		if isinstance(data, int):
			print("marshal_float on int value! Converting to float...")
			data = float(data)

		if not isinstance(data, float):
			print("Error! marshal_float called on non-float value!")
			raise TypeError
			
		return struct.pack('<d', data)
	

	@staticmethod
	def marshal_enum(data):
		
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

if __name__ == '__main__':
<<<<<<< HEAD
	print(Marshaller.marshal_string("Hello There").hex())
	print(Marshaller.marshal_int(1024).hex())
	print(Marshaller.marshal_float(5.1).hex())
	# print(Marshaller.marshal_object(BalanceMessage("Sid", 10853693087894514759, "password123")).hex())
	# print(compile_message(12, BalanceMessage("Sid", 10853693087894514759, "password123")).hex())
	print(Marshaller.marshal_object(DepositMessage("Sid", 10853693087894514759, "password123", 1, 105.5)).hex())
	print(compile_message(16, DepositMessage("Sid", 10853693087894514759, "password123", 1, 105.5)))
	print(list(compile_message(20, CreateNewAccountOutput(10853693087894514759, "New account created with account number " + str(10853693087894514759)))))
	print(list(Marshaller.marshal_enum(CurrencyType(2))))
	print(list(compile_message(20, CreateNewAccountInput("Sid", "password", 105.5, CurrencyType(2)))))
	
=======
	ba = BankAccount("aks", 123, "pass")
	comp_ba = compile_message(1, ba)
	print(comp_ba)

	uncomp_ba = decompile_message(comp_ba)
	print(uncomp_ba)
>>>>>>> a98b2351d24273691764256ac4d7144f63806406
