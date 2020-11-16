## bot challenge
* përshëndetje
  - utter_përshëndetje
* bot_challenge
  - utter_jambot
* mirupafshim 
  - utter_mirupafshim

## kërkesë_dokumenti nuk ruhen të dhënat
* përshëndetje
  - utter_përshëndetje
* kërkesë
  - utter_kërkesëInfo
  - form_kerkese
  - form {"name": "form_kerkese"}
  - form {"name": null}
* mohim
  - form_feedback
  - form {"name": "form_feedback"}
  - form {"name": null}

## kërkesë_dokumenti ruhen te dhënat
* përshëndetje
  - utter_përshëndetje
* kërkesë
  - utter_kërkesëInfo
  - form_kerkese
  - form {"name": "form_kerkese"}
  - form {"name": null}
* pohim
  - action_ruajTeDhenat
  - utter_dickaTjeter
* mohim
  - form_feedback
  - form {"name": "form_feedback"}
  - form {"name": null}

## kërkesë_dokumenti ruhen te dhënat vazhdohet biseda
* përshëndetje
  - utter_përshëndetje
* kërkesë
  - utter_kërkesëInfo
  - form_kerkese
  - form {"name": "form_kerkese"}
  - form {"name": null}
* pohim
  - action_ruajTeDhenat
  - utter_dickaTjeter
* pohim
  - utter_methuaj

## bashkëbisedimet
* shërbimet OR orari OR dokumentaElektronike OR bursa OR kohëzgjatjaDokumentit
  - action_chitchat

## mbrojtja gjuhës së huaj
* mbrojtaGjuhesHuaj
  - action_mbrojtaGjuhesHuaj

## default fallback
* pakuptim
  - action_default_fallback