package com.paperse.acagraph.Datemodels.Readin;

import com.google.gson.annotations.SerializedName;

/**
 * Created by sunhaoran on 2018/3/11.
 */
public class confinfo {
    private String name;
    private String title;
    private String confname;
    private String href;
    private String confurl;
    @SerializedName("id")
    private String cid;
    private int ccid;

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

    public String getCid() {
        return cid;
    }

    public void setCid(String cid) {
        this.cid = cid;
    }

    public int getCcid() {
        return ccid;
    }

    public void setCcid(int ccid) {
        this.ccid = ccid;
    }
}
