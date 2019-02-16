<<<<<<< HEAD
// +build !go1.7

package pq

import "crypto/tls"

// Renegotiation is not supported by crypto/tls until Go 1.7.
func sslRenegotiation(*tls.Config) {}
=======
// +build !go1.7

package pq

import "crypto/tls"

// Renegotiation is not supported by crypto/tls until Go 1.7.
func sslRenegotiation(*tls.Config) {}
>>>>>>> cbfed986b26b1d577ce60de9423248b7ad5a777c
