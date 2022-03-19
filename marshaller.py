import sys
import json
import struct
from marshalable import Marshalable


class Marshaller:

	@staticmethod
	def marshal(data, numBytes = 8):
		# primitive data types
		if (type(data) == str):
			return Marshaller.marshal_string(data)
		if (type(data) == int):
			return Marshaller.marshal_int(data, numBytes)
		if (type(data) == float):
			return Marshaller.marshal_float(data)

		# user-defined classes
		return Marshaller.marshal_object(data)
		
	
	@staticmethod
	def marshal_string(data):
		strlen = len(data) + 1
		strlen = Marshaller.marshal_int(strlen, 4)
		# result = struct.pack('s', data)
		result = data.encode('utf-8')

		result = strlen + result
		return result


	@staticmethod
	def marshal_int(data, numBytes = 8):
		if numBytes == 4:
			return struct.pack('<i', data)
		
		return struct.pack('<q', data)

	
	@staticmethod
	def marshal_float(data):
		return struct.pack('<d', data)
	

	@staticmethod
	def marshal_object(data):
		result = bytes()
		
		objType = data.object_type()
		result += Marshaller.marshal_int(objType, 4)

		fieldDict = data.get_fields()
		for fieldId, fieldVal in fieldDict.items():
			result += Marshaller.marshal_int(fieldId, 4)
			result += Marshaller.marshal(fieldVal)

		return result


def compile_message(messageID: int, object: Marshalable):
	result = bytes()
	
	marshalledMessageID = Marshaller.marshal(messageID, 4)
	marshalledObject = Marshaller.marshal(object)

	result += marshalledMessageID + marshalledObject

	messageLen = len(result)
	marshalledMessageLen = Marshaller.marshal(messageLen, 4)
	
	result = marshalledMessageLen + result

	return result


if __name__ == '__main__':
	b = BankAccount("Aks", 123456, "password")

	msg = compile_message(0, b)
	print(msg)

		