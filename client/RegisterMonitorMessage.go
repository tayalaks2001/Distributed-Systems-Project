package main

import "reflect"

type RegisterMonitorMessage struct {
	name            string
	accNum          uint64
	password        string
	durationMinutes uint64
}

func (rmm RegisterMonitorMessage) get_fields() map[int]any {
	m := make(map[int]any)
	m[0] = rmm.name
	m[1] = rmm.accNum
	m[2] = rmm.password
	m[3] = rmm.durationMinutes
	return m
}

func (rmm RegisterMonitorMessage) from_fields(fields map[int]any) Marshalable {
	return RegisterMonitorMessage{fields[0].(string), fields[1].(uint64), fields[2].(string), fields[3].(uint64)}
}

func (rmm RegisterMonitorMessage) get_field_types() map[int]reflect.Type {
	m := make(map[int]reflect.Type)
	m[0] = reflect.TypeOf(rmm.name)
	m[1] = reflect.TypeOf(rmm.accNum)
	m[2] = reflect.TypeOf(rmm.password)
	m[3] = reflect.TypeOf(rmm.durationMinutes)
	return m
}

func (rmm RegisterMonitorMessage) object_type() int {
	return 3
}