package main

import (
	"encoding/binary"
	"fmt"
	"math"
	"reflect"
)

type unmarshal_functions interface {
	unmarshal_string(message_len int, message []byte) string
	unmarshal_uint64(message []byte) uint64
	unmarshal_uint32(message []byte) uint32
	unmarshal_float(message []byte) float64
	unmarshal_object(message []byte) Marshalable
}

type unmarshaller struct {
	registry *Registry
}

func (um unmarshaller) unmarshal_string(message_len int, message []byte) string {
	if message_len != len(message) {
		fmt.Println("Error! unmarshal_string is called with an incorrect input!")
		return "Error"
	}
	return string(message)
}

func (um unmarshaller) unmarshal_uint64(message []byte) uint64 {
	return binary.LittleEndian.Uint64((message))
}

func (um unmarshaller) unmarshal_uint32(message []byte) uint32 {
	return binary.LittleEndian.Uint32((message))
}

func (um unmarshaller) unmarshal_float(message []byte) float64 {
	var uint64_bits uint64 = binary.LittleEndian.Uint64(message)
	return math.Float64frombits(uint64_bits)
}

func (um unmarshaller) unmarshal_object(message []byte) Marshalable {

	var object_id int = int(um.unmarshal_uint32(message[:4]))
	value, err := um.registry.Get(object_id)
	if err != nil {
		fmt.Printf("error: %s\n", err.Error())
		return nil
	}
	unwrapped_val := value.Unwrap()
	var object Marshalable = getMarshalableObject(unwrapped_val)//Note that at this stage, object is just a dummy to represent the type

	var fields_type_map map[int]reflect.Type = object.get_field_types() 
	var fields_map map[int]any = map[int]any{}

	var marshalled_object []byte = message[4:]
	var index int = 0
	for index < len(marshalled_object) {
		var field_id int = int(um.unmarshal_uint32(marshalled_object[index:index + 4]))
		index += 4
		var field_type reflect.Type = fields_type_map[field_id]
		var field_val any = nil
		if field_type == reflect.TypeOf(uint64(0)){
			field_val = um.unmarshal_uint64(marshalled_object[index:index+8])
			index += 8
		} else if field_type == reflect.TypeOf(float64(0)) {
			field_val = um.unmarshal_float(marshalled_object[index:index+8])
			index += 8
		} else if field_type == reflect.TypeOf("a") {
			var field_len int = int(um.unmarshal_uint32(marshalled_object[index:index+4]))
			field_val = um.unmarshal_string(field_len, marshalled_object[index+4:index+4+field_len])
			index += 4 + field_len
		} else {
			fmt.Println("Error! The field does not match any primitive datatype!")
			return nil
		}
		fields_map[field_id] = field_val
	}
	object = object.from_fields(fields_map) //here is where object gets its concrete values
	return object
}

func decompile_message(um unmarshal_functions, message []byte) (int, Marshalable){
	var message_len int = int(um.unmarshal_uint32(message[:4]))
	if len(message) - 4 != message_len{
		fmt.Println("Received message length does not match expected length!")
		return -1, nil
	}
	var message_id int = int(um.unmarshal_uint32(message[4:8]))
	var object Marshalable = um.unmarshal_object(message[8:])

	return message_id, object
}