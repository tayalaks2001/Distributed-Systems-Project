package main

import (
	"encoding/binary"
	"fmt"
	"math"
	"reflect"
)

type marshal_functions interface {
	marshal() []byte
	marshal_string(string_data string) []byte
	marshal_uint32(int_data uint32) []byte
	marshal_uint64(uint64_data uint64) []byte
	marshal_float(float_data float64) []byte
	marshal_struct(struct_data Marshalable) []byte
}

type marshaller struct {
}

func (m marshaller) marshal() []byte {
	bs := make([]byte, 8)
	return bs
}

func (m marshaller) marshal_uint32(int_data uint32) []byte {
	data := make([]byte, 4)
	binary.LittleEndian.PutUint32(data, int_data)
	return data
}

func (m marshaller) marshal_uint64(uint64_data uint64) []byte {
	data := make([]byte, 8)
	binary.LittleEndian.PutUint64(data, uint64_data)
	return data
}

func (m marshaller) marshal_float(float_data float64) []byte {
	data := make([]byte, 8)
	var uint64_float uint64 = math.Float64bits(float_data) 
	binary.LittleEndian.PutUint64(data, uint64_float)
	return data
}

func (m marshaller)marshal_string(string_data string) []byte {
	var str_len uint32 = uint32(len(string_data))
	var len_marshalled []byte = m.marshal_uint32(str_len)
	var str_marshalled []byte = []byte(string_data)
	return append(len_marshalled, str_marshalled...)
}

func (m marshaller)marshal_struct(struct_data Marshalable) []byte{
	data := make([]byte, 0)
	var obj_type int = struct_data.object_type()
	data = append(data, m.marshal_uint32(uint32(obj_type))...)
	var fields_map map[int]any = struct_data.get_fields()
	fmt.Println(fields_map)
	for field_id, field_val := range fields_map {
		data = append(data, m.marshal_uint32((uint32(field_id)))...)	
		switch v := field_val.(type){
			case uint64: data = append(data, m.marshal_uint64(field_val.(uint64))...)
			case float64: data = append(data, m.marshal_float(field_val.(float64))...)
			case string: data = append(data, m.marshal_string(field_val.(string))...)
		default: fmt.Println("An error occurred %v " + v.(string), field_val);
		}
	} 
	return data
}

func compile_message(m marshal_functions, message_id int, object Marshalable) []byte {
	result := make([]byte, 0)
	result = append(result, m.marshal_uint32(uint32(message_id))...)
	result = append(result, m.marshal_struct(object)...)
	var message_len uint32 = uint32(len(result))
	result = append(m.marshal_uint32(message_len), result...)

	return result
}

func printDetails(m marshal_functions) {
    fmt.Println((m.marshal_string("Hello There!")))
	fmt.Println((m.marshal_uint64(1024)))
	fmt.Println((m.marshal_float(5.1)))
	var qMessage Marshalable = QueryBalanceMessage{"Sid", uint64(10853693087894514759), "password123"}
	fmt.Println((m.marshal_struct(qMessage)))
	fmt.Println((compile_message(m, 12, qMessage)))
}

func generateRegistry(r *Registry) error {
	//r.Put(&foo{})
	r.Put(&QueryBalanceMessage{})
	return nil
}

func printUnmarshalDetails(um unmarshal_functions) {
	string_bytes := []byte{12, 0, 0, 0, 72, 101, 108, 108, 111, 32, 84, 104, 101, 114, 101, 33}
	uint64_bytes := []byte{0, 4, 0, 0, 0, 0, 0, 0}
	float64_bytes := []byte{102, 102, 102, 102, 102, 102, 20, 64}
	struct_bytes := []byte{90, 2, 0, 0, 2, 0, 0, 0, 71, 172, 16, 173, 91, 16, 160, 150, 3, 0, 0, 0, 11, 0, 0, 0, 112, 97, 115, 115, 119, 111, 114, 100, 49, 50, 51, 1, 0, 0, 0, 3, 0, 0, 0, 83, 105, 100}
	compiled_mssg_bytes := []byte{50, 0, 0, 0, 12, 0, 0, 0, 90, 2, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 83, 105, 100, 2, 0, 0, 0, 71, 172, 16, 173, 91, 16, 160, 150, 3, 0, 0, 0, 11, 0, 0, 0, 112, 97, 115, 115, 119, 111, 114, 100, 49, 50, 51}
	fmt.Println(um.unmarshal_uint64(uint64_bytes))
	fmt.Println(um.unmarshal_float(float64_bytes))
	var str_len int = int(um.unmarshal_uint32(string_bytes[0:4]))
	fmt.Println("String length: ", str_len)
	fmt.Println(um.unmarshal_string(str_len, string_bytes[4:]))
	var final_object Marshalable = um.unmarshal_object(struct_bytes)
	fmt.Println(final_object)
	fmt.Println(reflect.TypeOf(final_object))
	var message_id int = 0
	message_id, final_object = decompile_message(um, compiled_mssg_bytes)
	fmt.Println("Message ID: ", message_id)
	fmt.Println("Object: ", final_object)
} 

func main () {
	m := marshaller{}
	registry, err := NewRegistry(generateRegistry)
	if err != nil {
		fmt.Printf("error: %s\n", err.Error())
		return
	}
	fmt.Println(reflect.TypeOf("a"))
	um := unmarshaller{registry}
	// value, err := registry.Get(602)
	// if err != nil {
	// 	fmt.Printf("error: %s\n", err.Error())
	// 	return
	// }
	// i := value.Unwrap()
	// var object Marshalable = getMarshalableObject(i)	
	// fmt.Println(object.object_type())
	printDetails(m)
	printUnmarshalDetails(um)
}
