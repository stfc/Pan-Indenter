'/software/components/filecopy/services' =
npush(escape(CONDOR_LOCAL_CONFIG_FILE),
    nlist("config", CONDOR_LOCAL_CONFIG_CONTENTS,
        "owner", "root",
        "perms", "0644",
    )
);

'/software/components/dirperm/paths' = {
    foreach(k;directory;CONDOR_DIRECTORIES) {
        SELF[length(SELF)] = nlist(
            'path', directory,
            'owner' , CONDOR_USER+':'+CONDOR_GROUP,
            'perm', '0755',
            'type', 'd',
        );
    };
    SELF;
};

variable test = {
    if ( is_defined(test) ) {
        debug(test + ': configuring testing monitoring');
        test;
    } else {
        debug(test + ': testing monitoring disabled');
        undef;
    }
};
