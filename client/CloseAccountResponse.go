package main

import "reflect"

type CloseAccountResponse struct {
	accNum   uint64
	message string
}

func (car CloseAccountResponse) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = car.accNum
	m[1] = car.message
	return m
}

func (car CloseAccountResponse) from_fields(fields map[int]any) Marshalable{
	//return qMessage;
	return CloseAccountResponse{fields[0].(uint64), fields[1].(string)} 
}

func (car CloseAccountResponse) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(car.accNum)
	m[1] = reflect.TypeOf(car.message)
	return m
}

func (car CloseAccountResponse) object_type() int {
	return 8
}