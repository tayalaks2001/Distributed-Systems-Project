package main

import (
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"math"
)

// Interface to describe the functions to be implemented by the marshaller
type marshal_functions interface {
	marshal() []byte
	marshal_string(string_data string) []byte
	marshal_uint32(int_data uint32) []byte
	marshal_uint64(uint64_data uint64) []byte
	marshal_float(float_data float64) []byte
	marshal_struct(struct_data Marshalable) []byte
	marshal_enum(enum_data Marshalable) []byte
}

// Dummy struct to represent a marshaller object
type marshaller struct {
}

// Unimplemented function included in case of required extension at a later date
func (m marshaller) marshal() []byte {
	bs := make([]byte, 8)
	return bs
}

/*
Marsal unsigned 32-bit integer using binary package
Keyword arguments:
int_data: 32-bit value to be marshalled

Returns:
Marshalled 4-byte output
*/
func (m marshaller) marshal_uint32(int_data uint32) []byte {
	data := make([]byte, 4)
	binary.LittleEndian.PutUint32(data, int_data)
	return data
}

/*
Marsal unsigned 64-bit integer using binary package
Keyword arguments:
uint64_data: 64-bit value to be marshalled

Returns:
Marshalled 8-byte output
*/
func (m marshaller) marshal_uint64(uint64_data uint64) []byte {
	data := make([]byte, 8)
	binary.LittleEndian.PutUint64(data, uint64_data)
	return data
}

/*
Marsal 64-bit float using binary package
Keyword arguments:
float_data: 64-bit float to be marshalled

Returns:
Marshalled 8-byte output
*/
func (m marshaller) marshal_float(float_data float64) []byte {
	data := make([]byte, 8)
	var uint64_float uint64 = math.Float64bits(float_data)
	binary.LittleEndian.PutUint64(data, uint64_float)
	return data
}

/*
Marsal string using binary package
Keyword arguments:
string_data: string to be marshalled

Returns:
Marshalled string output
*/
func (m marshaller) marshal_string(string_data string) []byte {
	var str_len uint32 = uint32(len(string_data))
	var len_marshalled []byte = m.marshal_uint32(str_len)
	var str_marshalled []byte = []byte(string_data)
	return append(len_marshalled, str_marshalled...)
}

/*
Marsal objects implementing the Marshalable interface using binary package
Keyword arguments:
struct_data: struct to be marshalled

Returns:
Marshalled struct output
*/
func (m marshaller) marshal_struct(struct_data Marshalable) []byte {
	data := make([]byte, 0)
	var obj_type int = struct_data.object_type()
	data = append(data, m.marshal_uint32(uint32(obj_type))...)
	var fields_map map[int]any = struct_data.get_fields()
	fmt.Println(fields_map)
	for field_id, field_val := range fields_map {
		data = append(data, m.marshal_uint32((uint32(field_id)))...)
		switch v := field_val.(type) {
		case uint64:
			data = append(data, m.marshal_uint64(field_val.(uint64))...)
		case CurrencyType: 
			data = append(data, m.marshal_uint32(uint32(field_val.(CurrencyType).object_type()))...)
			data = append(data, m.marshal_uint32(field_val.(CurrencyType).getValue())...)
		case float64:
			data = append(data, m.marshal_float(field_val.(float64))...)
		case string:
			data = append(data, m.marshal_string(field_val.(string))...)
		default:
			fmt.Println("An error occurred %v "+v.(string), field_val)
		}
	}
	return data
}

/*
Marsal enum using binary package
Keyword arguments:
enum_data: enum to be marshalled

Returns:
Marshalled 8-byte output
*/
func (m marshaller) marshal_enum(enum_data Marshalable) []byte {
	data := make([]byte, 0)
	data = append(data, m.marshal_uint32(uint32(enum_data.object_type()))...)
	data = append(data, m.marshal_uint32(enum_data.get_fields()[0].(uint32))...)
	return data
}

/*
Compile final message to be sent over the network
Keyword arguments:
m: marshaller that implements the marshal_functions interface
message_id: id set by client
object: response object (implementing Marshalable) to be marshalled

Returns:
Complete marshalled message
*/
func compile_message(m marshal_functions, message_id int, object Marshalable) []byte {
	result := make([]byte, 0)
	result = append(result, m.marshal_uint32(uint32(message_id))...)
	result = append(result, m.marshal_struct(object)...)
	var message_len uint32 = uint32(len(result))
	result = append(m.marshal_uint32(message_len), result...)

	return result
}

// Testing function
func printDetails(m marshal_functions) {
	fmt.Println((m.marshal_string("Hello There!")))
	fmt.Println((m.marshal_uint64(1024)))
	fmt.Println((m.marshal_float(5.1)))
	var qMessage Marshalable = QueryBalanceMessage{"Sid", uint64(10853693087894514759), "password123"}
	var dMessage Marshalable = DepositMessage{DWBaseMessage{"Sid", uint64(10853693087894514759), "password123", SGD, 105.5}}
	var cMessage Marshalable = CreateBankAccountMessage{"Sid", "password", 105.5, USD}
	fmt.Println((m.marshal_struct(qMessage)))
	fmt.Println((hex.EncodeToString(m.marshal_struct(dMessage))))
	fmt.Println(compile_message(m, 20, cMessage))
	fmt.Println((hex.EncodeToString(compile_message(m, 12, qMessage))))
	fmt.Println((compile_message(m, 16, dMessage)))
}

// Function to generate the registry of all the custom structs used in code
func generateRegistry(r *Registry) error {
	//r.Put(&foo{})
	r.Put(&CloseAccountMessage{})
	r.Put(&CloseAccountResponse{})
	r.Put(&QueryBalanceMessage{})
	r.Put(&QueryBalanceResponse{})
	r.Put(&CreateBankAccountMessage{})
	r.Put(&CreateBankAccountResponse{})
	r.Put(&DepositMessage{})
	r.Put(&WithdrawMessage{})
	r.Put(&ErrorMessage{})
	r.Put(&MonitorResponse{})
	r.Put(&RegisterMonitorMessage{})
	r.Put(&RegisterMonitorOutput{})
	r.Put(&TransferMessage{})
	r.Put(CurrencyType(0))
	return nil
}

// func main () {
// 	m := marshaller{}
// 	registry, err := NewRegistry(generateRegistry)
// 	if err != nil {
// 		fmt.Printf("error: %s\n", err.Error())
// 		return
// 	}
// 	fmt.Println(reflect.TypeOf("a"))
// 	um := unmarshaller{registry}
// 	// value, err := registry.Get(602)
// 	// if err != nil {
// 	// 	fmt.Printf("error: %s\n", err.Error())
// 	// 	return
// 	// }
// 	// i := value.Unwrap()
// 	// var object Marshalable = getMarshalableObject(i)
// 	// fmt.Println(object.object_type())
// 	printDetails(m)
// 	printUnmarshalDetails(um)
// }
