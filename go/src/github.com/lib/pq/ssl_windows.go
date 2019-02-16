<<<<<<< HEAD
// +build windows

package pq

import "os"

// sslCertificatePermissions checks the permissions on user-supplied certificate
// files. In libpq, this is a no-op on Windows.
func sslCertificatePermissions(cert, key os.FileInfo) {}
=======
// +build windows

package pq

import "os"

// sslCertificatePermissions checks the permissions on user-supplied certificate
// files. In libpq, this is a no-op on Windows.
func sslCertificatePermissions(cert, key os.FileInfo) {}
>>>>>>> cbfed986b26b1d577ce60de9423248b7ad5a777c
