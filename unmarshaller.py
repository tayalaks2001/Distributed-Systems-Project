import struct
from enum import Enum
from messages.marshalable import MarshalableRegistry
from currency_type import CurrencyType

class Unmarshaller:

    @staticmethod
    def unmarshal_int(message):
        """
		Unmarshal int using the struct unpack method.
		Keyword arguments:
		message: byte array to be unmarshalled

		Returns: 
		Int object/value error if byte array can't be unpacked
		"""

        if len(message) == 4:
            return struct.unpack('<i', message)[0]
        elif len(message) == 8:
            return struct.unpack('<Q', message)[0]
        else:
            print("Error! unmarshal_int is called with an incorrect input!")
            raise ValueError
    

    @staticmethod
    def unmarshal_float(message):
        """
		Unmarshal float using the struct unpack method.
		Keyword arguments:
		message: byte array to be unmarshalled

		Returns: 
		Float object/value error if byte array can't be unpacked
		"""

        if len(message) != 8:
            print("Error! unmarshal_float is called with an incorrect input!")
            raise ValueError
        
        return struct.unpack('<d', message)[0]
    

    @staticmethod
    def unmarshal_string(message_len, message):
        """
		Unmarshal string using the string decode method.
		Keyword arguments:
		message: byte array to be unmarshalled

		Returns: 
		String object/value error if byte array can't be unpacked
		"""

        if message_len != len(message):
            print("Error! unmarshal_string is called with an incorrect input!")
            raise ValueError

        return message.decode('utf-8')

    
    @staticmethod
    def unmarshal_enum(message):
        """
		Unmarshal enum object.
		Keyword arguments:
		message: byte array to be unmarshalled

		Returns: 
		enum object/value error if byte array can't be unpacked
		"""

        if len(message) != 8:
            print("Error! unmarshal_enum is called with an incorrect input!")
            raise ValueError
        
        object_id = Unmarshaller.unmarshal_int(message[:4])
        if object_id == CurrencyType.object_type():
            object_class = CurrencyType
        else:
            print("No enum type exists with the given object type!")
            raise ValueError

        value = Unmarshaller.unmarshal_int(message[4:8])

        object = object_class(value)

        return object
    

    @staticmethod
    def unmarshal_object(message):
        """
		Unmarshal marshalled object.
		Keyword arguments:
		message: byte array to be unmarshalled

		Returns: 
		Object of instance of subtype marshalable/type error if byte array can't be unpacked
		"""

        object_id = Unmarshaller.unmarshal_int(message[:4])
        object_class = MarshalableRegistry.get_registry()[object_id]

        marshalled_object = message[4:]
        fields_type_dict = object_class.get_field_types()
        fields_dict = {}

        index = 0
        while index < len(marshalled_object):
            field_id = Unmarshaller.unmarshal_int(marshalled_object[index:index+4])
            index += 4
            field_type = fields_type_dict[field_id]
            if field_type == int:
                field_val = Unmarshaller.unmarshal_int(marshalled_object[index:index+8])
                index += 8
            elif field_type == float:
                field_val = Unmarshaller.unmarshal_float(marshalled_object[index:index+8])
                index += 8
            elif field_type == str:
                field_len = Unmarshaller.unmarshal_int(marshalled_object[index:index+4])
                field_val = Unmarshaller.unmarshal_string(field_len, marshalled_object[index+4:index+4+field_len])
                index += 4 + field_len
            elif field_type == Enum:
                field_val = Unmarshaller.unmarshal_enum(marshalled_object[index:index+8])
                index += 8
            else:
                print("Error! The field does not match any primitive datatype!")
                raise(TypeError)
            
            fields_dict[field_id] = field_val
        

        unmarshalled_object = object_class.from_fields(fields_dict)
        return unmarshalled_object



def decompile_message(message: bytes) -> list:
    """
	Decompile message received from client.
	Keyword arguments:
	message: byte array to be decompiled

	Returns: 
	Message id and object/value error if object is in improper format.
	"""

    try:   
        message_len = Unmarshaller.unmarshal_int(message[:4])
        # Verify message length
        if len(message)-4 != message_len:
            print("Received message length does not match expected length!")
            raise ValueError

        message_id = Unmarshaller.unmarshal_int(message[4:8])
        object = Unmarshaller.unmarshal_object(message[8:])

        return message_id, object


    except IndexError:
        print("Message is not in proper format!")
        return None
