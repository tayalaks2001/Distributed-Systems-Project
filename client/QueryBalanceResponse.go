package main

import "reflect"

type QueryBalanceResponse struct {
	balance float64
	message string
}

func (q QueryBalanceResponse) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = q.balance
	m[1] = q.message
	return m
}

func (q QueryBalanceResponse) from_fields(fields map[int]any) Marshalable{
	//return qMessage;
	return QueryBalanceResponse{fields[0].(float64), fields[1].(string)} 
}

func (q QueryBalanceResponse) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(q.balance)
	m[1] = reflect.TypeOf(q.message)
	return m
}

func (q QueryBalanceResponse) object_type() int {
	return 610
}