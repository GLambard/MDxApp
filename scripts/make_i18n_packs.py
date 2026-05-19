#!/usr/bin/env python3
"""Generate scripts/i18n_locale_packs.py from translations + locale data."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANS_PATH = ROOT / "Assets" / "translations.json"
OUT_PATH = ROOT / "scripts" / "i18n_locale_packs.py"
BUILD_MOD = ROOT / "scripts" / "_build_i18n_locale_packs.py"

import importlib.util

_spec = importlib.util.spec_from_file_location("_build", BUILD_MOD)
_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_build)

GAPS = _build.GAPS
_phase2_block = _build._phase2_block
_about_block = _build._about_block
_versions_table = _build._versions_table


def _merge_ui_p2_about(
    ui: dict[str, str],
    p2_kwargs: dict[str, str],
    about_kwargs: dict[str, str],
    f5: str,
    title: str,
    what_hdr: str,
) -> dict[str, str]:
    ab = _about_block(
        what_text=about_kwargs["what_text"],
        feat_hdr=about_kwargs["feat_hdr"],
        f1=about_kwargs["f1"],
        f2=about_kwargs["f2"],
        f3=about_kwargs["f3"],
        f4=about_kwargs["f4"],
        f6=about_kwargs["f6"],
        excl_hdr=about_kwargs["excl_hdr"],
        excl1=about_kwargs["excl1"],
        excl2=about_kwargs["excl2"],
        excl3=about_kwargs["excl3"],
        sup_hdr=about_kwargs["sup_hdr"],
        sup_txt=about_kwargs["sup_txt"],
        ver_hdr=about_kwargs["ver_hdr"],
        ver_tbl=about_kwargs["ver_tbl"],
        src_hdr=about_kwargs["src_hdr"],
        src_txt=about_kwargs["src_txt"],
        caut_hdr=about_kwargs["caut_hdr"],
        dev_hdr=about_kwargs["dev_hdr"],
        dev_msg=about_kwargs["dev_msg"],
        contact_title=about_kwargs.get("contact_title"),
    )
    ab["page_about_feature_5"] = f5
    ab["page_about_title"] = title
    ab["page_about_what_heading"] = what_hdr
    return {**ui, **_phase2_block(**p2_kwargs), **ab}


# ---------------------------------------------------------------------------
# Full packs (117 keys each)
# ---------------------------------------------------------------------------

def _pack_italiano() -> dict[str, str]:
    ui = {
        "page1_title": "Assistente diagnostico",
        "bmc_0": "Manteniamo MDxApp gratuito!",
        "bmc_1": "Cliccando qui:",
        "bmc_2": "Oppure usa questo codice QR:",
        "page1_header": "Assistente diagnostico medico",
        "page1_subheader": "Scopri il futuro della sanità con il nostro strumento <br>di diagnosi medica e controllo sintomi basato su ChatGPT.",
        "htu_0": "Come usare questa app:",
        "htu_1": "Compila il referto qui sotto (alcuni sintomi sono obbligatori)",
        "htu_2": "Controlla il riepilogo del referto",
        "htu_3": "Invia il referto (nessun dato fornito viene salvato o conmotionato)",
        "report_header": "Referto",
        "gender": "Sesso",
        "male": "Maschio",
        "female": "Femmina",
        "age": "Età",
        "pregnant": "Gravidanza",
        "no": "No",
        "yes": "Sì",
        "history": "Anamnesi",
        "hist_example": "(Esempio: festival musicale all'aperto in Nord America, bevande e sigarette con amici con sintomi simili)",
        "hist_ph": "nessuno",
        "hist_help": "Inserire le informazioni di background note del paziente, incluse patologie pregresse, farmaci, storia familiare, stile di vita e altre informazioni utili a diagnosi e trattamento",
        "symptoms": "Sintomi",
        "symp_example": "(Esempio: febbre alta, letargia, mal di testa e dolore addominale da due giorni)",
        "symp_ph": "nessuno",
        "symp_help": "Elencare tutti i sintomi che indicano una condizione medica sottostante",
        "exam": "Esito dell'esame",
        "exam_example": "(Esempio: lesioni petecchiali su palmi e piante, punture di insetti)",
        "exam_ph": "nessuno",
        "exam_help": "Elencare tutte le informazioni raccolte con ispezione, palpazione, percussione e auscultazione durante l'esame",
        "lab": "Risultati di laboratorio",
        "lab_example": "(Esempio: IgE > 3000 UI/m)",
        "lab_ph": "nessuno",
        "lab_help": "Elencare gli esami su campioni biologici o tessuti per diagnosi, monitoraggio o trattamento (sangue, urine, imaging, biopsie, ecc.)",
        "summary": "Riepilogo",
        "vissum_patient": "Paziente: ",
        "vissum_yrsold": " anni",
        "vissum_pregnancy": "Gravidanza: ",
        "vissum_history": "Anamnesi: ",
        "vissum_symp": "Sintomi: ",
        "vissum_exam": "Esito dell'esame: ",
        "vissum_lab": "Risultati di laboratorio: ",
        "submit": "INVIA",
        "submit_help": "Invia il referto per la diagnosi",
        "diagnostic": "Diagnosi",
        "none": "nessuno",
        "submit_warning": "Inserire almeno alcuni sintomi prima dell'invio.",
        "submit_wait": "Attendere prego...",
        "caution": "Messaggio di avvertenza",
        "caution_message": "Sebbene l'app supporti le decisioni cliniche e il controllo dei sintomi, la diagnosi finale deve essere formulata da un professionista abilitato. Si consiglia di richiedere valutazioni aggiuntive prima di qualsiasi trattamento.  ",
        "no_response": "Il server non risponde o è sovraccarico... Riprovare.",
        "no_diagnostic": "Nessuna diagnosi ancora. Compilare il referto e fare clic su INVIA sopra.",
        "language_selection": "Seleziona una lingua:",
        "dx_primary": "Diagnosi principale",
        "dx_confidence": "Confidenza",
        "dx_differential": "Diagnosi differenziali",
        "dx_next_steps": "Passi successivi raccomandati",
        "dx_considerations": "Considerazioni importanti",
        "dx_reasoning": "Ragionamento clinico",
        "dx_confidence_high": "ALTA",
        "dx_confidence_medium": "MEDIA",
        "dx_confidence_low": "BASSA",
        "dx_fallback_notice": "Formato strutturato non disponibile; diagnosi in testo semplice.",
        "invest": "Investi nella tua salute e sostieni la nostra missione di mantenere MDxApp gratuito!",
        "dx_download_pdf": "Scarica report PDF",
        "medications": "Farmaci",
        "contact_form_name_ph": "Il tuo nome",
        "contact_form_email_ph": "La tua email",
        "contact_form_message_ph": "Il tuo messaggio",
        "contact_form_submit": "Invia",
    }
    ui["htu_3"] = ui["htu_3"].replace("conmotionato", "condiviso")
    p2 = dict(
        pdf_title="Rapporto di diagnosi medica MDxApp",
        pdf_patient="Riepilogo paziente",
        pdf_gen="Generato",
        dx_icd10="ICD-10",
        dx_refs="Riferimenti",
        dx_evidence_disc="I riferimenti sono solo a scopo educativo; verificare con un clinico.",
        dx_imaging="Risultati di imaging",
        dx_drug="Avvisi sui farmaci",
        meds_ex="(Esempio: metformina, lisinopril)",
        meds_ph="nessuno",
        meds_help="Elencare i farmaci attuali, uno per riga o separati da virgole",
        img_hdr="Immagine medica (opzionale)",
        img_consent="Le immagini non vengono archiviate. Solo uso educativo — non è un referto radiologico.",
        img_lbl="Tipo di immagine",
        img_skin="Pelle / eruzione",
        img_xray="Radiografia",
        img_ecg="Tracciato ECG",
        img_lab="Foto referto di laboratorio",
        img_other="Altro",
        img_upload="Carica immagine (JPG/PNG, max 5 MB)",
        img_large="L'immagine supera il limite di 5 MB.",
        img_warn="Usare formato JPG o PNG.",
        dx_ev_none="Non sono stati forniti riferimenti verificabili per questo caso.",
    )
    about = dict(
        what_text="MDxApp è un **assistente gratuito alla diagnosi medica** per clinici, studenti e pazienti. Organizza i sintomi e restituisce una **valutazione preliminare assistita dall'IA** tramite [OpenAI](https://openai.com/) **{model}**, con output strutturati e utilizzabili.",
        feat_hdr="Funzionalità attuali (v{version})",
        f1="**Diagnosi strutturata** — diagnosi principale, differenziali, passi successivi, considerazioni, confidenza, ragionamento clinico",
        f2="**Download report PDF** — riepilogo conmotionable dopo ogni valutazione",
        f3="**Riferimenti educativi** — link bibliografici con PMID o URL verificabili (PubMed)",
        f4="**Note sulla sicurezza dei farmaci** — avvisi di interazione (OpenFDA + IA)",
        f6="**Privacy first** — nessun dato paziente sui nostri server; ogni sessione è effimera",
        excl_hdr="Non incluso (per scelta)",
        excl1="**Caricamento immagini mediche** — disabilitato durante la validazione di sicurezza e accuratezza",
        excl2="**Codici di fatturazione regionali (ICD-10, ecc.)** — nascosti perché i sistemi di codifica variano per paese",
        excl3="**Diagnosi finale** — richiede sempre un clinico abilitato",
        sup_hdr="Sostieni il progetto",
        sup_txt="L'app usa l'API OpenAI, con un costo reale per richiesta. Le donazioni tramite **Buy Me a Coffee** (barra laterale) aiutano a mantenere MDxApp gratuito. Grazie per il supporto.",
        ver_hdr="Cronologia versioni",
        ver_tbl=_versions_table("Versione", "Data", "Punti salienti",
            "Modello predefinito **gpt-5.4-nano**, About/Contact localizzati, 15 lingue, RTL arabo",
            "Fase 2: export PDF, riferimenti, controlli farmaci, UI diagnosi strutturata",
            "Architettura modulare, output strutturati, test automatizzati",
            "UI multilingue, integrazione ChatGPT", "Prima release pubblica"),
        src_hdr="Fonti",
        src_txt="- Codice sorgente: [github.com/GLambard/MDxApp](https://github.com/GLambard/MDxApp)\n- Casi d'esempio da materiale didattico pubblico (es. [@BrownJHM](https://twitter.com/BrownJHM)).",
        caut_hdr="Avvertenza",
        dev_hdr="Messaggio dello sviluppatore",
        dev_msg="> Grazie per usare MDxApp. Questo progetto nasce nel tempo libero per rendere il pensiero diagnostico più accessibile nel mondo. Il tuo feedback e il supporto con un caffè lo tengono attivo.\n>\n> — **Guillaume Lambard**, designer e sviluppatore di soluzioni IA",
        contact_title="Contatti",
    )
    about["f2"] = about["f2"].replace("conmotionable", "condivisibile")
    return _merge_ui_p2_about(
        ui, p2, about,
        "**Oltre 15 lingue** — interfaccia globale con RTL per l'arabo",
        "Informazioni su MDxApp",
        "Cos'è MDxApp?",
    )


def _std_about(
    what: str, feat: str, f1: str, f2: str, f3: str, f4: str, f5: str, f6: str,
    excl_hdr: str, excl1: str, excl2: str, excl3: str,
    sup_hdr: str, sup_txt: str, ver_hdr: str,
    vt: tuple[str, str, str, str, str, str, str],
    src_hdr: str, src_txt: str, caut: str, dev_hdr: str, dev_msg: str,
    contact: str,
) -> dict[str, str]:
    return dict(
        what_text=what, feat_hdr=feat, f1=f1, f2=f2, f3=f3, f4=f4, f6=f6,
        excl_hdr=excl_hdr, excl1=excl1, excl2=excl2, excl3=excl3,
        sup_hdr=sup_hdr, sup_txt=sup_txt, ver_hdr=ver_hdr,
        ver_tbl=_versions_table(*vt),
        src_hdr=src_hdr, src_txt=src_txt, caut_hdr=caut, dev_hdr=dev_hdr,
        dev_msg=dev_msg, contact_title=contact,
    )


def _std_p2(
    pdf_title: str, pdf_pt: str, pdf_gen: str, icd: str, refs: str, disc: str,
    img: str, drug: str, meds_ex: str, meds_ph: str, meds_help: str,
    img_hdr: str, img_consent: str, img_lbl: str, skin: str, xray: str, ecg: str,
    lab: str, other: str, upload: str, large: str, warn: str, ev_none: str,
) -> dict[str, str]:
    return dict(
        pdf_title=pdf_title, pdf_patient=pdf_pt, pdf_gen=pdf_gen,
        dx_icd10=icd, dx_refs=refs, dx_evidence_disc=disc,
        dx_imaging=img, dx_drug_alerts=drug, meds_ex=meds_ex, meds_ph=meds_ph,
        meds_help=meds_help, img_hdr=img_hdr, img_consent=img_consent,
        img_lbl=img_lbl, img_skin=skin, img_xray=xray, img_ecg=ecg,
        img_lab=lab, img_other=other, img_upload=upload, img_large=large,
        img_warn=warn, dx_ev_none=ev_none,
    )


# Load extended packs from generated JSON (created on first run if missing)
_CACHE = ROOT / "scripts" / ".locale_packs_cache.json"


def _load_or_build_cache() -> dict[str, dict[str, str]]:
    if _CACHE.exists():
        return json.loads(_CACHE.read_text(encoding="utf-8"))
    from scripts import _locale_packs_bulk as bulk  # noqa: WPS433

    data = bulk.build_all()
    _CACHE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def build_locale_packs() -> dict[str, dict[str, str]]:
    trans = json.loads(TRANS_PATH.read_text(encoding="utf-8"))
    en = trans["English"]
    keys = list(en.keys())
    packs: dict[str, dict[str, str]] = {}

    for lang in ("Français", "Español", "Deutsch", "日本語"):
        block = dict(trans[lang])
        block.update(GAPS[lang])
        packs[lang] = {k: block[k] for k in keys}

    packs["Italiano"] = _pack_italiano()

    cached = _load_or_build_cache()
    for lang, block in cached.items():
        if lang not in packs:
            packs[lang] = block

    return packs


def write_output(packs: dict[str, dict[str, str]]) -> None:
    """Write importable module with LOCALE_PACKS as a Python literal (safe for all Unicode)."""
    packs_literal = json.dumps(packs, ensure_ascii=False, indent=4)
    header = textwrap.dedent(
        '''\
        """Complete locale packs for MDxApp (117 keys × 14 languages, English excluded)."""

        from __future__ import annotations

        from typing import Any

        LOCALE_PACKS: dict[str, dict[str, str]] = '''
    )
    footer = textwrap.dedent(
        '''\


        def merge_into(base: dict[str, Any]) -> dict[str, Any]:
            """Merge LOCALE_PACKS into a translations.json-style dict."""
            english = base.get("English", {})
            for lang, pack in LOCALE_PACKS.items():
                if lang not in base:
                    base[lang] = dict(english)
                base[lang].update(pack)
            return base


        if __name__ == "__main__":
            for lang, block in LOCALE_PACKS.items():
                print(f"{lang}: {len(block)} keys")
        '''
    )
    OUT_PATH.write_text(header + packs_literal + footer, encoding="utf-8")


def main() -> None:
    packs = build_locale_packs()
    for lang, block in sorted(packs.items()):
        print(f"{lang}: {len(block)} keys")
    write_output(packs)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
