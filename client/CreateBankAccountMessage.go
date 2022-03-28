package main

import "reflect"

type CreateBankAccountMessage struct {
	name         string
	accNum       uint64
	password     string
	currencyType CurrencyType
}

func (cMessage CreateBankAccountMessage) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = cMessage.name
	m[1] = cMessage.accNum
	m[2] = cMessage.password
	m[3] = cMessage.currencyType
	return m
}

func (cMessage CreateBankAccountMessage) from_fields(fields map[int]any) Marshalable {
	return CreateBankAccountMessage{fields[0].(string), fields[1].(uint64), fields[2].(string), fields[3].(CurrencyType)}
}

func (cMessage CreateBankAccountMessage) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(cMessage.name)
	m[1] = reflect.TypeOf(cMessage.accNum)
	m[2] = reflect.TypeOf(cMessage.password)
	m[3] = reflect.TypeOf(cMessage.currencyType)
	return m
}

func (cMessage CreateBankAccountMessage) object_type() int {
	return 1
}