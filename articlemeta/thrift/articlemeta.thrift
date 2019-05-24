const string VERSION = "1.2.0"

exception ValueError {
    1: string message,
}

exception ServerError {
    1: string message,
}

exception Unauthorized {
    1: string message,
}

struct collection {
    1: string code
    2: string acronym
    3: optional string acronym2letters
    4: optional string status
    5: string domain
    6: string name
    7: bool has_analytics
    8: optional bool is_active
    9: optional string type
}

struct article_identifiers {
    1: string code,
    2: string collection,
    3: string processing_date,
    4: string aid,
    5: string doi,
}

struct issue_identifiers {
    1: string code,
    2: string collection,
    3: string processing_date
}

struct journal_identifiers {
    1: string code,
    2: string collection,
    3: string processing_date
}

struct event_document {
    1: string code,
    2: string collection,
    3: string event,
    4: string date
}

struct event_issue {
    1: string code,
    2: string collection,
    3: string event,
    4: string date
}

struct event_journal {
    1: string code,
    2: string collection,
    3: string event,
    4: string date
}

service ArticleMeta {
    string getInterfaceVersion(),
    list<event_document> article_history_changes(1: string collection, 2: string event, 3: string code, 4: string from_date, 5: string until_date, 6: i32 limit, 7: i32 offset) throws (1: ValueError value_err, 2:ServerError server_err),
    list<event_issue> issue_history_changes(1: string collection, 2: string event, 3: string code, 4: string from_date, 5: string until_date, 6: i32 limit, 7: i32 offset) throws (1: ValueError value_err, 2:ServerError server_err),
    list<event_journal> journal_history_changes(1: string collection, 2: string event, 3: string code, 4: string from_date, 5: string until_date, 6:i32 limit, 7: i32 offset) throws (1: ValueError value_err, 2:ServerError server_err),
    collection get_collection(1: string code) throws (1: ValueError value_err, 2:ServerError server_err),
    string get_article(1: string code, 2: string collection, 3: bool replace_journal_metadata, 4: string fmt, 5: bool body) throws (1: ValueError value_err, 2:ServerError server_err),
    string get_issue(1: string code, 2: string collection, 3: bool replace_journal_metadata) throws (1: ValueError value_err, 2:ServerError server_err),
    string get_journal(1: string code, 2: string collection) throws (1: ValueError value_err, 2:ServerError server_err),
    list<article_identifiers> get_article_identifiers(1: optional string collection, 2: optional string issn, 3: optional string from_date, 4: optional string until_date, 5: i32 limit, 6: i32 offset, 7: optional string extra_filter) throws (1:ValueError value_err, 2:ServerError server_err),
    string get_articles(1: optional string collection, 2: optional string issn, 3: optional string from_date, 4: optional string until_date, 5: i32 limit, 6: i32 offset, 7: optional string extra_filter, 8: optional bool replace_journal_metadata, 9: optional bool body) throws (1:ValueError value_err, 2:ServerError server_err),
    list<issue_identifiers> get_issue_identifiers(1: optional string collection, 2: optional string issn, 3: optional string from_date, 4: optional string until_date, 5: i32 limit, 6: i32 offset, 7: optional string extra_filter) throws (1:ValueError value_err, 2:ServerError server_err),
    string get_issues(1: optional string collection, 2: optional string issn, 3: optional string from_date, 4: optional string until_date, 5: i32 limit, 6: i32 offset, 7: optional string extra_filter) throws (1:ValueError value_err, 2:ServerError server_err),
    list<journal_identifiers> get_journal_identifiers(1: optional string collection, 2: optional string issn, 3: i32 limit, 4: i32 offset, 5: optional string extra_filter) throws (1: ValueError value_err, 2:ServerError server_err),
    list<collection> get_collection_identifiers() throws(1: ServerError server_err),
    bool set_doaj_id(1: string code, 2: string collection, 3: string doaj_id, 4: string admintoken) throws (1: ValueError value_err, 2:ServerError server_err, 3:Unauthorized unauthorized_access),
    bool set_aid(1: string code, 2: string collection, 3: string aid, 4: string admintoken) throws (1: ValueError value_err, 2:ServerError server_err, 3:Unauthorized unauthorized_access),
    bool exists_article(1: string code, 2: string collection) throws (1: ValueError value_err, 2:ServerError server_err),
    bool exists_issue(1: string code, 2: string collection) throws (1: ValueError value_err, 2:ServerError server_err),
    bool exists_journal(1: string code, 2: string collection) throws (1: ValueError value_err, 2:ServerError server_err),
    bool is_name_suffix(1: string suffix) throws (1: ValueError value_err, 2:ServerError server_err),
    string delete_journal(1: string code, 2: string collection, 3: string admintoken) throws (1:ServerError server_err, 2:Unauthorized unauthorized_access),
    string delete_issue(1: string code, 2: string collection, 3: string admintoken) throws (1:ServerError server_err, 2:Unauthorized unauthorized_access),
    string delete_article(1: string code, 2: string collection, 3: string admintoken) throws (1:ServerError server_err, 2:Unauthorized unauthorized_access),
    string add_journal(1: string metadata, 2: string admintoken) throws (1: ValueError value_err, 2:ServerError server_err, 3:Unauthorized unauthorized_access),
    string add_issue(1: string metadata, 2: string admintoken) throws (1: ValueError value_err, 2:ServerError server_err, 3:Unauthorized unauthorized_access),
    string add_article(1: string metadata, 2: string admintoken) throws (1: ValueError value_err, 2:ServerError server_err, 3:Unauthorized unauthorized_access),
    void add_name_suffix(1: string metadata, 2: string admintoken) throws (1: ValueError value_err, 2:ServerError server_err, 3:Unauthorized unauthorized_access),
    string get_issue_code_from_label(1: string label, 2: string journal_code, 3: string collection) throws (1: ValueError value_err, 2:ServerError server_err)
}
