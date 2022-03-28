package main

import "reflect"

type ErrorMessage struct {
	errCode   uint64
	message string
}

func (err ErrorMessage) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = err.errCode
	m[1] = err.message
	return m
}

func (err ErrorMessage) from_fields(fields map[int]any) Marshalable{
	return ErrorMessage{fields[0].(uint64), fields[1].(string)} 
}

func (err ErrorMessage) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(err.errCode)
	m[1] = reflect.TypeOf(err.message)
	return m
}

func (err ErrorMessage) object_type() int {
	return 7
}