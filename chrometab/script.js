chrome.contextMenus.removeAll();
chrome.contextMenus.create({
    id: "some-command",
    title: "Sandy Loader - получить все файлы с сайта",
    }
);
chrome.contextMenus.onClicked.addListener(function() {
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    chrome.tabs.create({
        url: "http://127.0.0.1:8000/"
    });
    fetch('http://127.0.0.1:8000?par=' + tabs[0].url).then(r => r.text()).then(result => {
});
});

    }
);
