<<<<<<< HEAD
// Package pq is a pure Go Postgres driver for the database/sql package.

// +build darwin dragonfly freebsd linux nacl netbsd openbsd solaris rumprun

package pq

import (
	"os"
	"os/user"
)

func userCurrent() (string, error) {
	u, err := user.Current()
	if err == nil {
		return u.Username, nil
	}

	name := os.Getenv("USER")
	if name != "" {
		return name, nil
	}

	return "", ErrCouldNotDetectUsername
}
=======
// Package pq is a pure Go Postgres driver for the database/sql package.

// +build darwin dragonfly freebsd linux nacl netbsd openbsd solaris rumprun

package pq

import (
	"os"
	"os/user"
)

func userCurrent() (string, error) {
	u, err := user.Current()
	if err == nil {
		return u.Username, nil
	}

	name := os.Getenv("USER")
	if name != "" {
		return name, nil
	}

	return "", ErrCouldNotDetectUsername
}
>>>>>>> cbfed986b26b1d577ce60de9423248b7ad5a777c
