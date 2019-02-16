<<<<<<< HEAD
// +build !windows

package pq

import "os"

// sslCertificatePermissions checks the permissions on user-supplied certificate
// files. The key file should have very little access.
//
// libpq does not check key file permissions on Windows.
func sslCertificatePermissions(cert, key os.FileInfo) {
	kmode := key.Mode()
	if kmode != kmode&0600 {
		panic(ErrSSLKeyHasWorldPermissions)
	}
}
=======
// +build !windows

package pq

import "os"

// sslCertificatePermissions checks the permissions on user-supplied certificate
// files. The key file should have very little access.
//
// libpq does not check key file permissions on Windows.
func sslCertificatePermissions(cert, key os.FileInfo) {
	kmode := key.Mode()
	if kmode != kmode&0600 {
		panic(ErrSSLKeyHasWorldPermissions)
	}
}
>>>>>>> cbfed986b26b1d577ce60de9423248b7ad5a777c
