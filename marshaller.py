import sys
import json
import struct
from marshalable import Marshalable

class Marshaller:

	@staticmethod
	def marshal(message, numBytes = 8):

		res = bytes()

		if (type(message) == str):
			return Marshaller.marshal_string(message)
		if (type(message) == int):
			return Marshaller.marshal_int(message, numBytes)
		if (type(message) == float):
			return Marshaller.marshal_float(message)
		
		return TypeError
		
	
	@staticmethod
	def marshal_string(message):
		return message.encode('utf-8')
	
	@staticmethod
	def marshal_int(message, numBytes):
		return message.to_bytes(numBytes, byteorder = 'big', signed = False)
	
	@staticmethod
	def marshal_float(message, numBytes):
		# return bytes(struct.pack('f', message))

		intVal = int(message)
		floatVal = message - intVal

		result = bytes()
		result += Marshaller.marshal_int(intVal, )
	


class Message:

	def __init__(self, messageID, messageContent, account):
		self.messageID = messageID
		self.messageContent = messageContent
		self.messageLength = len(messageContent)
		self.accountObj = account.serialize()
		self.checkSum = b'00'
		


	@staticmethod
	def marshal(messageID, message, delimiter = ' '):

		# encode message length
		messageLength = len(message)
		messageLength = messageLength.to_bytes(4, byteorder = 'big', signed = False)

		
		# encode message ID
		messageID = messageID.to_bytes(4, byteorder = 'big', signed = True)

		
		# encode message content
		message = message.encode('utf-8')

		
		# encode delimiter between message fields
		delimiter = delimiter.encode('utf-8')

		
		# combine all encoded fields
		bytestream = messageLength + delimiter + messageID + delimiter + message

		
		return bytestream