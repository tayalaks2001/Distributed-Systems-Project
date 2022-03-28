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

func (m marshaller) marshal_string(string_data string) []byte {
	var str_len uint32 = uint32(len(string_data))
	var len_marshalled []byte = m.marshal_uint32(str_len)
	var str_marshalled []byte = []byte(string_data)
	return append(len_marshalled, str_marshalled...)
}

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
			data = append(data, m.marshal_uint64(field_val.(uint64))...)
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
	var dMessage Marshalable = DepositMessage{DWBaseMessage{"Sid", uint64(10853693087894514759), "password123", CurrencyType(1), 105.5}}
	fmt.Println((m.marshal_struct(qMessage)))
	fmt.Println((hex.EncodeToString(m.marshal_struct(dMessage))))
	fmt.Println((hex.EncodeToString(compile_message(m, 12, qMessage))))
	fmt.Println((hex.EncodeToString(compile_message(m, 16, dMessage))))
}

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
