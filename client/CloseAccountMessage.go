package main

import "reflect"

type CloseAccountMessage struct {
	name     string
	accNum   uint64
	password string
}

func (cam CloseAccountMessage) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = cam.name
	m[1] = cam.accNum
	m[2] = cam.password
	return m
}

func (cam CloseAccountMessage) from_fields(fields map[int]any) Marshalable{
	//return qMessage;
	return CloseAccountMessage{fields[0].(string), fields[1].(uint64), fields[2].(string)} 
}

func (cam CloseAccountMessage) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(cam.name)
	m[1] = reflect.TypeOf(cam.accNum)
	m[2] = reflect.TypeOf(cam.password)
	return m
}

func (cam CloseAccountMessage) object_type() int {
	return 9
}