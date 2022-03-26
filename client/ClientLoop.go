package main

import (
	"context"
	"fmt"
	"io"
	"net"
	"time"
)

func client(ctx context.Context, address string, reader io.Reader) (err error) {

	raddr, err := net.ResolveUDPAddr("udp", address)
	if err != nil {
		return
	}

	conn, err := net.DialUDP("udp", nil, raddr)
	if err != nil {
		return
	}

	defer conn.Close()

	doneChan := make(chan error, 1)

	go func() {
		n, err := io.Copy(conn, reader)
		if err != nil {
			doneChan <- err
			return
		}

		maxBufferSize := 1024
		timeout := time.Second

		fmt.Printf("packet-written: bytes=%d\n", n)

		buffer := make([]byte, maxBufferSize)

		// Set a deadline for the ReadOperation so that we don't
		// wait forever for a server that might not respond on
		// a resonable amount of time.
		deadline := time.Now().Add(timeout)
		err = conn.SetReadDeadline(deadline)
		if err != nil {
			doneChan <- err
			return
		}

		nRead, addr, err := conn.ReadFrom(buffer)
		if err != nil {
			doneChan <- err
			return
		}

		fmt.Printf("packet-received: bytes=%d from=%s\n",
			nRead, addr.String())

		doneChan <- nil
	}()

	select {
	case <-ctx.Done():
		fmt.Println("cancelled")
		err = ctx.Err()
	case err = <-doneChan:
	}

	return
}
