//adapted from : https://github.com/AlexsJones/go-type-registry

//Crucial Note: All the maps here have values which are reflect.Type. In order to obtain the type itself and initialize a new var, refer to the following example (syntax may be slightly wrong):

// m = q.get_fields()
// intType1 := m[1].Elem() //let's say that the first attribute of marshalable q is indeed an int
// intPtr1 = reflect.New(intType1)
// firstAttr = intPtr1.Elem().Interface().(int) //this variable will be an integer initialized with the default value of 0. We can then proceed to manipulate it how we desire

package main

import (
	"errors"
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