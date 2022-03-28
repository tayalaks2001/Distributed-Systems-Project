package main

type MessageResponse interface {
	extractMssg() string
}