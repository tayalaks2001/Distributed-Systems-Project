package main

import "reflect"

type QueryBalanceMessage struct {
	name     string
	accNum   uint64
	password string
}

func (q QueryBalanceMessage) get_fields() map[int]any {
	m := make(map[int]any)
	m[1] = q.name
	m[2] = q.accNum
	m[3] = q.password
	return m
}

func (q QueryBalanceMessage) from_fields(fields map[int]any) Marshalable{
	//return qMessage;
	return QueryBalanceMessage{fields[1].(string), fields[2].(uint64), fields[3].(string)} 
}

func (q QueryBalanceMessage) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[1] = reflect.TypeOf(q.name)
	m[2] = reflect.TypeOf(q.accNum)
	m[3] = reflect.TypeOf(q.password)
	return m
}

func (q QueryBalanceMessage) object_type() int {
	return 602
}