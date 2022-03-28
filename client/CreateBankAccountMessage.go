package main

import "reflect"

type CreateBankAccountMessage struct {
	name         string
	password     string
	initBalance  float64
	currencyType CurrencyType
}

func (cMessage CreateBankAccountMessage) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = cMessage.name
	m[1] = cMessage.password
	m[2] = cMessage.initBalance
	m[3] = cMessage.currencyType
	return m
}

func (cMessage CreateBankAccountMessage) from_fields(fields map[int]any) Marshalable {
	return CreateBankAccountMessage{fields[0].(string), fields[1].(string), fields[2].(float64), fields[3].(CurrencyType)}
}

func (cMessage CreateBankAccountMessage) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(cMessage.name)
	m[1] = reflect.TypeOf(cMessage.password)
	m[2] = reflect.TypeOf(cMessage.initBalance)
	m[3] = reflect.TypeOf(cMessage.currencyType)
	return m
}

func (cMessage CreateBankAccountMessage) object_type() int {
	return 1
}