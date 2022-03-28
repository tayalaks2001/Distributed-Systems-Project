package main

import "reflect"

type MonitorResponse struct {
	message string
}

func (mr MonitorResponse) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = mr.message
	return m
}

func (mr MonitorResponse) from_fields(fields map[int]any) Marshalable{
	//return qMessage;
	return MonitorResponse{fields[0].(string)} 
}

func (mr MonitorResponse) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(mr.message)
	return m
}

func (mr MonitorResponse) object_type() int {
	return 999
}

func (mr MonitorResponse) extractMssg() string {
	return mr.message
}