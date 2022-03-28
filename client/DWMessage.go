package main

import "reflect"

type DWBaseMessage struct {
	name         string
	accNum       uint64
	password     string
	currencyType CurrencyType
	amount       float64
}

func (dwm DWBaseMessage) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = dwm.name
	m[1] = dwm.accNum
	m[2] = dwm.password
	m[3] = dwm.currencyType
	m[4] = dwm.amount
	return m
}

func (dwm DWBaseMessage) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(dwm.name)
	m[1] = reflect.TypeOf(dwm.accNum)
	m[2] = reflect.TypeOf(dwm.password)
	m[3] = reflect.TypeOf(dwm.currencyType)
	m[4] = reflect.TypeOf(dwm.amount)
	return m
}

type DepositMessage struct {
	DWBaseMessage
}

type WithdrawMessage struct {
	DWBaseMessage
}

func (dMessage DepositMessage) from_fields(fields map[int]any) Marshalable {
	return DepositMessage{DWBaseMessage{fields[0].(string), fields[1].(uint64), fields[2].(string), fields[3].(CurrencyType), fields[4].(float64)}}
}

func (dMessage DepositMessage) object_type() int {
	return 600
}

func (wMessage WithdrawMessage) from_fields(fields map[int]any) Marshalable {
	return WithdrawMessage{DWBaseMessage{fields[0].(string), fields[1].(uint64), fields[2].(string), fields[3].(CurrencyType), fields[4].(float64)}}
}

func (wMessage WithdrawMessage) object_type() int {
	return 601
}
