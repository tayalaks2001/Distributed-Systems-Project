package main

import "reflect"

type TransferMessage struct {
	name            string
	accNum          uint64
	password        string
	currencyType    CurrencyType
	transferAmount  float64
	recipientAccNum uint64
}

func (tm TransferMessage) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = tm.name
	m[1] = tm.accNum
	m[2] = tm.password
	m[3] = tm.currencyType
	m[4] = tm.transferAmount
	m[5] = tm.recipientAccNum
	return m
}

func (tm TransferMessage) from_fields(fields map[int]any) Marshalable {
	//return qMessage;
	return TransferMessage{fields[0].(string), fields[1].(uint64), fields[2].(string), fields[3].(CurrencyType), fields[4].(float64), fields[5].(uint64)}
}

func (tm TransferMessage) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(tm.name)
	m[1] = reflect.TypeOf(tm.accNum)
	m[2] = reflect.TypeOf(tm.password)
	m[3] = reflect.TypeOf(tm.currencyType)
	m[4] = reflect.TypeOf(tm.transferAmount)
	m[5] = reflect.TypeOf(tm.recipientAccNum)
	return m
}

func (tm TransferMessage) object_type() int {
	return 5
}