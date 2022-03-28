//adapted from : https://github.com/AlexsJones/go-type-registry

package main

import (
	"errors"
	"fmt"
	"log"
	"reflect"
)

type Marshalable interface {
	object_type() int
	get_fields() map[int]any 
	from_fields(map[int]any) Marshalable
	get_field_types() map[int]reflect.Type
}

//Entry is a utility structure for holding type information for reflection
type Entry struct {
	Name    string
	RefType reflect.Type
}

//Unwrap brings the entry back into a real object
func (e *Entry) Unwrap() interface{} {
	return reflect.New(e.RefType).Elem().Interface()
}

//Registry is a utility structure for holding type information for reflection
type Registry struct {
	storedEntries map[int]*Entry
}

//Put will register a type against an int
func (r *Registry) Put(m Marshalable) {
	var object_type int = m.object_type()
	t := reflect.TypeOf(m)
	e := &Entry{RefType: t, Name: t.String()}
	log.Println("Registering as " + t.String())
	log.Println(reflect.TypeOf(m))
	r.storedEntries[object_type] = e
}

//Get will return a new instance of type if avialable
func (r *Registry) Get(object_type int) (*Entry, error) {
	e := r.storedEntries[object_type]
	if e == nil {
		return nil, errors.New("Not found")
	}
	return e, nil
}

//NewRegistry takes optional functions that can manipulate the object initialised
func NewRegistry(options ...func(*Registry) error) (*Registry, error) {
	r := &Registry{storedEntries: make(map[int]*Entry)}
	for _, op := range options {
		err := op(r)
		if err != nil {
			return nil, err
		}
	}
	return r, nil
}

func getMarshalableObject(unwrapped_val interface{}) Marshalable {
	var object Marshalable = nil
	switch unwrapped_val.(type) {
		//The type is a pointer to the foo object
		case *CloseAccountMessage:
			object = CloseAccountMessage{}
		case *CloseAccountResponse:
			object = CloseAccountResponse{}
		case *CreateBankAccountMessage:
			object = CreateBankAccountMessage{}
		case *CreateBankAccountResponse:
			object = CreateBankAccountResponse{}
		case *DepositMessage:
			object = DepositMessage{}
		case *WithdrawMessage:
			object = WithdrawMessage{}
		case *ErrorMessage:
			object = ErrorMessage{}
		case *MonitorResponse:
			object = MonitorResponse{}
		case *QueryBalanceMessage:
			object = QueryBalanceMessage{}
		case *QueryBalanceResponse:
			object = QueryBalanceResponse{}
		case *RegisterMonitorMessage:
			object = RegisterMonitorMessage{}
		case *RegisterMonitorOutput:
			object = RegisterMonitorOutput{}
		case *TransferMessage:
			object = TransferMessage{}
		case CurrencyType:
			object = CurrencyType(0)
		default: 
			fmt.Println("No object with specified ID found")
		}
	return object
}
