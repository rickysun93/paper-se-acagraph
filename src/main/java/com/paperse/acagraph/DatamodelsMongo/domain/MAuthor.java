package com.paperse.acagraph.DatamodelsMongo.domain;

import javax.persistence.Id;

/**
 * Created by sunhaoran on 2018/2/28.
 */
public class MAuthor {
    @Id
    private String id;

    private String name;

    private String namelower;

    private String org;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getNamelower() {
        return namelower;
    }

    public void setNamelower(String namelower) {
        this.namelower = namelower;
    }

    public String getOrg() {
        return org;
    }

    public void setOrg(String org) {
        this.org = org;
    }
}
