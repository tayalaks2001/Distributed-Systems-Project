package main

import (
	"fmt"
)

type marshal_functions interface {
	marshal() []byte
	marshal_string(string_data string) []byte
	// marshal_num() []byte
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

// func (m marshaller) marshal_num [N uint64 | float64](num_data N) []byte {
// 	data := make([]byte, 8)

// 	var uint_data uint64 = 0

// 	if (reflect.TypeOf(num_data).Kind() == reflect.Uint64){
// 		uint_data = uint64(num_data)
// 	} else if (reflect.TypeOf(num_data).Kind() == reflect.Float64) {
// 		uint_data = math.Float64bits(float64(num_data))
// 	}
// 	binary.LittleEndian.PutUint64(data, uint_data)
// 	return data
// }

func (m marshaller)marshal_string(string_data string) []byte {
	return []byte(string_data)
}

func printDetails(m marshal_functions) {
    fmt.Println(m.marshal_string("Hello There"))
}

func main () {
	data := make([]byte, 0)
	m := marshaller{data}
	printDetails(m)
}
