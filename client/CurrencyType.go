package main

import (
	"reflect"
)

var refMap map[CurrencyType]uint32 = map[CurrencyType]uint32{
	CurrencyType(0): 1,
	CurrencyType(1): 2,
	CurrencyType(2): 3,
}

type CurrencyType uint64

const
(
	SGD CurrencyType = iota 
	USD 
	INT
)

func (c CurrencyType) object_type() int {
	return 10
}

func (c CurrencyType) get_fields() map[int]any {
	return map[int]any{
		0: int(c),
	}
}

func (c CurrencyType) from_fields(fields map[int]any) Marshalable {
	return CurrencyType(fields[0].(int))
}

func (c CurrencyType) get_field_types() map[int]reflect.Type {
	return nil
}

func (c CurrencyType) getValue() uint32 {
	return refMap[c]
}

// func (c CurrencyType) getString(val int) string {
// 	var finalKey string = ""
// 	for key, value :=  range currencyTypeMap {
// 		if (val == value){
// 			finalKey = key
// 			break
// 		}
// 	}
// 	return finalKey
// }
