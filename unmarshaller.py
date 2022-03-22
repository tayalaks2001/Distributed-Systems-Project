import struct
from marshalable import MarshalableRegistry

class Unmarshaller:

    @staticmethod
    def unmarshal(message):
        ...
    
    @staticmethod
    def unmarshal_int(message):

        if len(message) == 4:
            return struct.unpack('<i', message)[0]
        elif len(message) == 8:
            return struct.unpack('<q', message)[0]
        else:
            print("Error! unmarshal_int is called with an incorrect input!")
            raise ValueError
    

    @staticmethod
    def unmarshal_float(message):
        
        if len(message) != 8:
            print("Error! unmarshal_float is called with an incorrect input!")
            raise ValueError
        
        return struct.unpack('<d', message)[0]
    

    @staticmethod
    def unmarshal_string(message_len, message):

        if message_len != len(message):
            print("Error! unmarshal_string is called with an incorrect input!")
            raise ValueError

        return message.decode('utf-8')
    

    @staticmethod
    def unmarshal_object(message):
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
            else:
                print("Error! The field does not match any primitive datatype!")
                raise(TypeError)
            
            fields_dict[field_id] = field_val
        

        unmarshalled_object = object_class.from_fields(fields_dict)
        return unmarshalled_object



def decompile_message(message: bytes) -> list:
    
    try:   
        message_len = Unmarshaller.unmarshal_int(message[:4])
        # Verify message length
        if len(message)-4 != message_len:
            print("Received message length does not match expected length!")
            raise ValueError

        message_id = Unmarshaller.unmarshal_int(message[4:8])
        object = Unmarshaller.unmarshal_object(message[8:])
        object.message_id = message_id

        return object


    except IndexError:
        print("Message is not in proper format!")
        return None
