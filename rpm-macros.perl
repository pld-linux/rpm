# Perl specific macro definitions.
# To make use of these macros insert the following line into your spec file:
# %include @RPMCONFIGDIR@/macros.perl

%define		__find_requires	@RPMCONFIGDIR@/find-perl-requires
%define		__find_provides	@RPMCONFIGDIR@/find-perl-provides

%define		perl_privlib	%(eval "`%{__perl} -V:installprivlib`"; echo $installprivlib)
%define		perl_archlib	%(eval "`%{__perl} -V:installarchlib`"; echo $installarchlib)
%define		perl_vendorlib	%(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define		perl_vendorarch	%(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)
%define		perl_sitelib	%(eval "`%{__perl} -V:installsitelib`"; echo $installsitelib)
%define		perl_sitearch	%(eval "`%{__perl} -V:installsitearch`"; echo $installsitearch)

