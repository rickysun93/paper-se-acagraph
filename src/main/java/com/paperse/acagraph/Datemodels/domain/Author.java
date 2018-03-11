package com.paperse.acagraph.Datemodels.domain;

import javax.persistence.*;
import javax.validation.constraints.NotNull;

/**
 * Created by sunhaoran on 2018/2/28.
 */
@Entity
public class Author {
    @Id
    @NotNull
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private String name;

    @Column(name="name_lower")
    private String namelower;

    private String org;

    public int getId() {
        return id;
    }

    public void setId(int id) {
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
