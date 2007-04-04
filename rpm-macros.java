%define	__java_provides	%{nil}
%define	__java_requires	/usr/lib/rpm/java-find-requires

# rpm itself doesn't recognize .jar and .class
%define	_use_internal_dependency_generator  0

%define	__find_provides    %{__java_provides}
%define	__find_requires    %{__java_requires}
