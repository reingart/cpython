"""macresource - Locate and open the resources needed for a script."""

from Carbon import Res
import os
import sys

class ArgumentError(TypeError): pass
class ResourceFileNotFoundError(ImportError): pass

def need(restype, resid, filename=None, modname=None):
	"""Open a resource file, if needed. restype and resid
	are required parameters, and identify the resource for which to test. If it
	is available we are done. If it is not available we look for a file filename
	(default: modname with .rsrc appended) either in the same folder as
	where modname was loaded from, or otherwise across sys.path.
	
	Returns the refno of the resource file opened (or None)"""

	if modname is None and filename is None:
		raise ArgumentError, "Either filename or modname argument (or both) must be given"
	
	if type(resid) is type(1):
		try:
			h = Res.GetResource(restype, resid)
		except Res.Error:
			pass
		else:
			return None
	else:
		try:
			h = Res.GetNamedResource(restype, resid)
		except Res.Error:
			pass
		else:
			return None
			
	# Construct a filename if we don't have one
	if not filename:
		if '.' in modname:
			filename = modname.split('.')[-1] + '.rsrc'
		else:
			filename = modname + '.rsrc'
	
	# Now create a list of folders to search
	searchdirs = []
	if modname == '__main__':
		# If we're main we look in the current directory
		searchdirs = [os.curdir]
	if sys.modules.has_key(modname):
		mod = sys.modules[modname]
		if hasattr(mod, '__file__'):
			searchdirs = [os.path.split(mod.__file__)[0]]
	if not searchdirs:
		searchdirs = sys.path
	
	# And look for the file
	for dir in searchdirs:
		pathname = os.path.join(dir, filename)
		if os.path.exists(pathname):
			break
	else:
		raise ResourceFileNotFoundError, filename
	
	refno = open_pathname(pathname)
	
	# And check that the resource exists now
	if type(resid) is type(1):
		h = Res.GetResource(restype, resid)
	else:
		h = Res.GetNamedResource(restype, resid)
	return refno
	
def open_pathname(pathname, verbose=0):
	"""Open a resource file given by pathname, possibly decoding an
	AppleSingle file"""
	try:
		refno = Res.FSpOpenResFile(pathname, 1)
	except Res.Error, arg:
		if arg[0] in (-37, -39):
			# No resource fork. We may be on OSX, and this may be either
			# a data-fork based resource file or a AppleSingle file
			# from the CVS repository.
			try:
				refno = Res.FSOpenResourceFile(pathname, u'', 1)
			except Res.Error, arg:
				if arg[0] != -199:
					# -199 is "bad resource map"
					raise
			else:
				return refno
			# Finally try decoding an AppleSingle file
			pathname = _decode(pathname, verbose=verbose)
			refno = Res.FSOpenResourceFile(pathname, u'', 1)
		else:
			raise
	return refno
	
def _decode(pathname, verbose=0):
	# Decode an AppleSingle resource file, return the new pathname.
	newpathname = pathname + '.df.rsrc'
	if os.path.exists(newpathname) and \
			os.stat(newpathname).st_mtime >= os.stat(pathname).st_mtime:
		return newpathname
	if verbose:
		print 'Decoding', pathname
	import applesingle
	applesingle.decode(pathname, newpathname, resonly=1)
	return newpathname
	
	