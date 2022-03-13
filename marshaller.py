import sys
import json


class BankAccount:

	def __init__(self, acctNumber, name, amount):
		self.acctNumber = acctNumber
		self.name = name
		self.amount = amount

	def serialize(self):
		fieldsDict = {"acctNumber": self.acctNumber, "name": self.name, "amount": self.amount}
		fieldsJSON = json.dumps(fieldsDict)
		return fieldsJSON



class Message:

	def __init__(self, messageID, messageContent, account: BankAccount):
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
		# endianness depends on interpreter
		message = message.encode('utf-8')

		
		# encode delimiter between message fields
		delimiter = delimiter.encode('utf-8')

		
		# combine all encoded fields
		bytestream = messageLength + delimiter + messageID + delimiter + message

		
		return bytestream