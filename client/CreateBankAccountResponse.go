package main

import "reflect"

type CreateBankAccountResponse struct {
	accNum   uint64
	message string
}

func (car CreateBankAccountResponse) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = car.accNum
	m[1] = car.message
	return m
}

func (car CreateBankAccountResponse) from_fields(fields map[int]any) Marshalable{
	//return qMessage;
	return CreateBankAccountResponse{fields[0].(uint64), fields[1].(string)} 
}

func (car CreateBankAccountResponse) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(car.accNum)
	m[1] = reflect.TypeOf(car.message)
	return m
}

func (car CreateBankAccountResponse) object_type() int {
	return 2
}

func (car CreateBankAccountResponse) extractMssg() string {
	return car.message
}