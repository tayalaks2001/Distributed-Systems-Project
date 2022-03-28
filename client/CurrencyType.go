package main

import "reflect"

type CurrencyType uint64

const (
	SGD CurrencyType = iota
	USD
	INR
)

func (c CurrencyType) object_type() int {
	return -1
}

func (c CurrencyType) get_fields() map[int]any {
	return nil
}

func (c CurrencyType) from_fields(fields map[int]any) Marshalable {
	return CurrencyType(1)
}

func (c CurrencyType) get_field_types() map[int]reflect.Type {
	return nil
}
