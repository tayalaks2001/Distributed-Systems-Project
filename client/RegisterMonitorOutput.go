package main

import "reflect"

type RegisterMonitorOutput struct {
	message string
}

func (rmo RegisterMonitorOutput) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] =  rmo.message
	return m
}

func (rmo RegisterMonitorOutput) from_fields(fields map[int]any) Marshalable{
	return RegisterMonitorOutput{fields[0].(string)} 
}

func (rmo RegisterMonitorOutput) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(rmo.message)
	return m
}

func (rmo RegisterMonitorOutput) object_type() int {
	return 4
}