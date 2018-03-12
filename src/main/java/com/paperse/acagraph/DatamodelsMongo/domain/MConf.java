package com.paperse.acagraph.DatamodelsMongo.domain;

import javax.persistence.Id;

/**
 * Created by sunhaoran on 2018/3/11.
 */
public class MConf {
    @Id
    private String id;

    private String name;
    private String title;
    private String confname;
    private String href;
    private String confurl;

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

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getConfname() {
        return confname;
    }

    public void setConfname(String confname) {
        this.confname = confname;
    }

    public String getHref() {
        return href;
    }

    public void setHref(String href) {
        this.href = href;
    }

    public String getConfurl() {
        return confurl;
    }

    public void setConfurl(String confurl) {
        this.confurl = confurl;
    }
}
