<<<<<<< HEAD
// +build go1.7

package pq

import "crypto/tls"

// Accept renegotiation requests initiated by the backend.
//
// Renegotiation was deprecated then removed from PostgreSQL 9.5, but
// the default configuration of older versions has it enabled. Redshift
// also initiates renegotiations and cannot be reconfigured.
func sslRenegotiation(conf *tls.Config) {
	conf.Renegotiation = tls.RenegotiateFreelyAsClient
}
=======
// +build go1.7

package pq

import "crypto/tls"

// Accept renegotiation requests initiated by the backend.
//
// Renegotiation was deprecated then removed from PostgreSQL 9.5, but
// the default configuration of older versions has it enabled. Redshift
// also initiates renegotiations and cannot be reconfigured.
func sslRenegotiation(conf *tls.Config) {
	conf.Renegotiation = tls.RenegotiateFreelyAsClient
}
>>>>>>> cbfed986b26b1d577ce60de9423248b7ad5a777c
