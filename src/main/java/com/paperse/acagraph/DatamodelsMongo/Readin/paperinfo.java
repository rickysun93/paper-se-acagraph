package com.paperse.acagraph.DatamodelsMongo.Readin;

import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;

/**
 * Created by sunhaoran on 2018/3/11.
 */
public class paperinfo {
    private String paperid;
    private String session;
    private String pdfUrl;
    private String name;
    private String url;
    @SerializedName("abstract")
    private String abs;
    private confinfo conf_info;
    private ArrayList<citation> citations;
    private ArrayList<reference> references;
    private ArrayList<author> authors;
    private ArrayList<String> citationsid;
    private ArrayList<String> referencesid;
    private ArrayList<String> authorsid;

    public String getPaperid() {
        return paperid;
    }

    public void setPaperid(String paperid) {
        this.paperid = paperid;
    }

    public ArrayList<String> getCitationsid() {
        return citationsid;
    }

    public void setCitationsid(ArrayList<String> citationsid) {
        this.citationsid = citationsid;
    }

    public ArrayList<String> getReferencesid() {
        return referencesid;
    }

    public void setReferencesid(ArrayList<String> referencesid) {
        this.referencesid = referencesid;
    }

    public String getSession() {
        return session;
    }

    public void setSession(String session) {
        this.session = session;
    }

    public String getPdfUrl() {
        return pdfUrl;
    }

    public void setPdfUrl(String pdfUrl) {
        this.pdfUrl = pdfUrl;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getAbs() {
        return abs;
    }

    public void setAbs(String abs) {
        this.abs = abs;
    }

    public confinfo getConf_info() {
        return conf_info;
    }

    public void setConf_info(confinfo conf_info) {
        this.conf_info = conf_info;
    }

    public ArrayList<citation> getCitations() {
        return citations;
    }

    public void setCitations(ArrayList<citation> citations) {
        this.citations = citations;
    }

    public ArrayList<reference> getReferences() {
        return references;
    }

    public void setReferences(ArrayList<reference> references) {
        this.references = references;
    }

    public ArrayList<author> getAuthors() {
        return authors;
    }

    public void setAuthors(ArrayList<author> authors) {
        this.authors = authors;
    }

    public ArrayList<String> getAuthorsid() {
        return authorsid;
    }

    public void setAuthorsid(ArrayList<String> authorsid) {
        this.authorsid = authorsid;
    }
}
