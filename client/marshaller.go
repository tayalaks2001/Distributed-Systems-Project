package main

import (
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"math"
)

type marshal_functions interface {
	marshal() []byte
	marshal_string(string_data string) []byte
	marshal_uint32(int_data uint32) []byte
	marshal_uint64(uint64_data uint64) []byte
	marshal_float(float_data float64) []byte
	marshal_struct(struct_data Marshalable) []byte
	//compile_message() []byte
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

func printDetails(m marshal_functions) {
    fmt.Println(hex.EncodeToString(m.marshal_string("Hello There")))
	fmt.Println(hex.EncodeToString(m.marshal_uint64(1024)))
	fmt.Println(hex.EncodeToString(m.marshal_float(5.1)))
	fmt.Println(hex.EncodeToString(m.marshal_struct(QueryBalanceMessage{"Sid", uint64(10853693087894514759), "password123"})))
}

func main () {
	m := marshaller{}
	printDetails(m)
}
