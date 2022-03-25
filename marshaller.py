import struct
from marshalable import Marshalable

class Marshaller:

	@staticmethod
	def marshal(data, num_bytes = 8):
		
		result = bytes()

		# primitive data types
		if isinstance(data, str):
			result = Marshaller.marshal_string(data)
		elif isinstance(data, int):
			result = Marshaller.marshal_int(data, num_bytes)
		elif isinstance(data, float):
			result = Marshaller.marshal_float(data)
		# user-defined classes
		else:
			result = Marshaller.marshal_object(data)

		return result
		
	
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

		return struct.pack('<q', data)

	
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
	#print(Marshaller.marshal_string("Hello There"))
	#print(Marshaller.marshal_int(1024))
	print(Marshaller.marshal_float(5.1))
