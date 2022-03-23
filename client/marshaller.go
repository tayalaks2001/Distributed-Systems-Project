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
	marshal_int (int_data uint64) []byte
	marshal_float (float_data float64) []byte
	//marshal_struct() []byte
	//compile_message() []byte
}

type marshaller struct {
	result []byte
}

func (m marshaller) marshal() []byte {
	bs := make([]byte, 8)
	return bs
}

func (m marshaller) marshal_int (int_data uint64) []byte {
	data := make([]byte, 8)
	binary.LittleEndian.PutUint64(data, int_data)
	return data
}

func (m marshaller) marshal_float (float_data float64) []byte {
	data := make([]byte, 8)
	var uint64_float uint64 = math.Float64bits(float_data) 
	binary.LittleEndian.PutUint64(data, uint64_float)
	return data
}

func (m marshaller)marshal_string(string_data string) []byte {
	var str_len uint64 = uint64(len(string_data) + 1)
	var len_marshalled []byte = m.marshal_int(str_len)
	var str_marshalled []byte = []byte(string_data)
	return append(len_marshalled, str_marshalled...)
}

func printDetails(m marshal_functions) {
    fmt.Println(m.marshal_string("Hello There"))
	fmt.Println(m.marshal_int(1024))
	//var a float64 = 1024.1022
	//fmt.Println(m.marshal_float(1024.1022))
	fmt.Println(hex.EncodeToString(m.marshal_float(5.1)))
}

func main () {
	data := make([]byte, 0)
	m := marshaller{data}
	printDetails(m)
}
