package main

import (
	"encoding/binary"
	"fmt"
	"math"
	"reflect"
)

// Interface that specifies the functions that must be implemented by the unmarshaller
type unmarshal_functions interface {
	unmarshal_string(message_len int, message []byte) string
	unmarshal_uint64(message []byte) uint64
	unmarshal_uint32(message []byte) uint32
	unmarshal_float(message []byte) float64
	unmarshal_enum(message []byte) Marshalable
	unmarshal_object(message []byte) Marshalable
}

// Unmarshaller struct containing the registry of all structs and objectIDs 
type unmarshaller struct {
	registry *Registry
}

/*
Unmarshal string using the string cast method.
Keyword arguments:
message_len: length of the string
message: byte array to be unmarshalled

Returns: 
String object
*/
func (um unmarshaller) unmarshal_string(message_len int, message []byte) string {
	if message_len != len(message) {
		fmt.Println("Error! unmarshal_string is called with an incorrect input!")
		return "Error"
	}
	return string(message)
}

/*
Unmarshal 8-byte unsigned int using the binary package.
Keyword arguments:
message: byte array to be unmarshalled

Returns: 
unsigned int 64 value
*/
func (um unmarshaller) unmarshal_uint64(message []byte) uint64 {
	return binary.LittleEndian.Uint64((message))
}

/*
Unmarshal 4-byte unsigned int using the binary package.
Keyword arguments:
message: byte array to be unmarshalled

Returns: 
unsigned int 32 value
*/
func (um unmarshaller) unmarshal_uint32(message []byte) uint32 {
	return binary.LittleEndian.Uint32((message))
}

/*
Unmarshal 8-byte float using the binary and math packages.
Keyword arguments:
message: byte array to be unmarshalled

Returns: 
64-bit float value
*/
func (um unmarshaller) unmarshal_float(message []byte) float64 {
	var uint64_bits uint64 = binary.LittleEndian.Uint64(message)
	return math.Float64frombits(uint64_bits)
}

/*
Unmarshal enum object
Keyword arguments:
message: byte array to be unmarshalled

Returns: 
enum object
*/
func (um unmarshaller) unmarshal_enum(message []byte) Marshalable {
	var value int = int(um.unmarshal_uint32(message[4:8]))
	return CurrencyType(0).from_fields(map[int]any{0: value})
}

/*
Unmarshal marshalled Marshalable object
Keyword arguments:
message: byte array to be unmarshalled

Returns: 
Marshalable object
*/
func (um unmarshaller) unmarshal_object(message []byte) Marshalable {

	var object_id int = int(um.unmarshal_uint32(message[:4]))
	value, err := um.registry.Get(object_id)
	if err != nil {
		fmt.Printf("error: %s\n", err.Error())
		return nil
	}
	unwrapped_val := value.Unwrap()
	var object Marshalable = getMarshalableObject(unwrapped_val) //Note that at this stage, object is just a dummy to represent the type

	var fields_type_map map[int]reflect.Type = object.get_field_types()
	var fields_map map[int]any = map[int]any{}

	var marshalled_object []byte = message[4:]
	var index int = 0

	for index < len(marshalled_object) {
		var field_id int = int(um.unmarshal_uint32(marshalled_object[index : index+4]))
		index += 4
		var field_type reflect.Type = fields_type_map[field_id]
		var field_val any = nil
		if field_type == reflect.TypeOf(uint64(0)) {
			field_val = um.unmarshal_uint64(marshalled_object[index : index+8])
			index += 8
		} else if field_type == reflect.TypeOf(float64(0)) {
			field_val = um.unmarshal_float(marshalled_object[index : index+8])
			index += 8
		} else if field_type == reflect.TypeOf("a") {
			var field_len int = int(um.unmarshal_uint32(marshalled_object[index : index+4]))
			field_val = um.unmarshal_string(field_len, marshalled_object[index+4:index+4+field_len])
			index += 4 + field_len
		} else if field_type == reflect.TypeOf(CurrencyType(0)) {
			field_val = um.unmarshal_enum(marshalled_object[index : index+8])
			index += 8
		} else {
			fmt.Println("Error! The field does not match any primitive datatype!")
			return nil
		}
		fields_map[field_id] = field_val
	}
	object = object.from_fields(fields_map) //here is where object gets its concrete values
	return object
}


/*
Decompile message received from server.
Keyword arguments:
um: unmarshaller object which implements the unmarshal_functions interface
message: byte array to be decompiled

Returns: 
Message id and Marshalable object
*/
func decompile_message(um unmarshal_functions, message []byte) (int, Marshalable) {
	var message_len int = int(um.unmarshal_uint32(message[:4]))
	if len(message)-4 != message_len {
		fmt.Println("Received message length does not match expected length!")
		return -1, nil
	}
	var message_id int = int(um.unmarshal_uint32(message[4:8]))
	var object Marshalable = um.unmarshal_object(message[8:])

	return message_id, object
}


// Testing function
func printUnmarshalDetails(um unmarshal_functions) {
	string_bytes := []byte{12, 0, 0, 0, 72, 101, 108, 108, 111, 32, 84, 104, 101, 114, 101, 33}
	uint64_bytes := []byte{0, 4, 0, 0, 0, 0, 0, 0}
	float64_bytes := []byte{102, 102, 102, 102, 102, 102, 20, 64}
	// struct_bytes := []byte{90, 2, 0, 0, 2, 0, 0, 0, 71, 172, 16, 173, 91, 16, 160, 150, 3, 0, 0, 0, 11, 0, 0, 0, 112, 97, 115, 115, 119, 111, 114, 100, 49, 50, 51, 1, 0, 0, 0, 3, 0, 0, 0, 83, 105, 100}
	// compiled_mssg_bytes := []byte{50, 0, 0, 0, 12, 0, 0, 0, 90, 2, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 83, 105, 100, 2, 0, 0, 0, 71, 172, 16, 173, 91, 16, 160, 150, 3, 0, 0, 0, 11, 0, 0, 0, 112, 97, 115, 115, 119, 111, 114, 100, 49, 50, 51}
	recvd_mssg_bytes := []byte{59, 0, 0, 0, 20, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 83, 105, 100, 1, 0, 0, 0, 8, 0, 0, 0, 112, 97, 115, 115, 119, 111, 114, 100, 2, 0, 0, 0, 0, 0, 0, 0, 0, 96, 90, 64, 3, 0, 0, 0, 10, 0, 0, 0, 2, 0, 0, 0}
	fmt.Println(um.unmarshal_uint64(uint64_bytes))
	fmt.Println(um.unmarshal_float(float64_bytes))
	var str_len int = int(um.unmarshal_uint32(string_bytes[0:4]))
	fmt.Println("String length: ", str_len)
	fmt.Println(um.unmarshal_string(str_len, string_bytes[4:]))
	var final_object Marshalable = nil //um.unmarshal_object(struct_bytes)
	// fmt.Println(final_object)
	// fmt.Println(reflect.TypeOf(final_object))
	var message_id int = 0
	// message_id, final_object = decompile_message(um, compiled_mssg_bytes)
	// fmt.Println("Message ID: ", message_id)
	// fmt.Println("Object: ", final_object)
	message_id, final_object = decompile_message(um, recvd_mssg_bytes)
	fmt.Println("Message ID: ", message_id)
	fmt.Println("Object: ", final_object)
}
