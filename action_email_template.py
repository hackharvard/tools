def build_action_email(
        *,
        action_name: str,
        action_description: str,
        action_link: str,
        action_buttonname: str,
        app_name: str,
        app_link: str,
        logo_url: str = "https://raw.githubusercontent.com/hackharvard/branding/refs/heads/main/static/logoForEmailNoBg.png",
        theme_color: str = "#e20029",
        background_color: str = "#f8f8f8",
        footer_year: int | None = None
) -> str:
    """
    Returns the full HTML email with the given values inserted.
    All inserted text is HTML-escaped.

    Required:
      action_name, action_description, action_link, action_buttonname, app_name, app_link

    Optional:
      logo_url, theme_color, background_color, footer_year
    """

    def paragraphize(text: str) -> str:
        # Escape first, then turn newlines into HTML
        safe = esc(text.strip())
        # Double newline -> paragraph split
        parts = [p.replace("\n", "<br>") for p in safe.split("\n\n")]
        return "".join(f"<p>{p}</p>" for p in parts if p)

    import html
    import re
    from datetime import date

    esc = html.escape

    tpl = """<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head>
    <title></title><!--[if !mso]><!-->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style type="text/css">
        #outlook a { padding: 0; }
        body { margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
        table, td { border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
        img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }
        p { display: block; margin: 13px 0; }
    </style>
    <!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
    <!--[if lte mso 11]><style type="text/css">.mj-outlook-group-fix { width:100% !important; }</style><![endif]-->
    <!--[if !mso]><!-->
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700" rel="stylesheet" type="text/css">
    <style type="text/css">@import url(https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700);</style>
    <!--<![endif]-->
    <style type="text/css">
        @media only screen and (min-width:480px) {
            .mj-column-per-100 { width: 100% !important; max-width: 100%; }
        }
    </style>
    <style media="screen and (min-width:480px)">
        .moz-text-html .mj-column-per-100 { width: 100% !important; max-width: 100%; }
    </style>
    <style type="text/css">
        @media only screen and (max-width:480px) {
            table.mj-full-width-mobile { width: 100% !important; }
            td.mj-full-width-mobile { width: auto !important; }
        }
    </style>
</head>

<body style="word-spacing:normal;background-color:#f8f8f8;">
    <div style="background-color:#f8f8f8;">
        <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" role="presentation" style="width:600px;" width="600" bgcolor="#ffffff" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
        <div style="background:#ffffff;background-color:#ffffff;margin:0px auto;max-width:600px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                <tbody><tr>
                    <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-left:0px;padding-right:0px;padding-top:0px;text-align:center;">
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                                <tbody><tr>
                                    <td align="center" style="font-size:0px;padding:10px 25px;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;word-break:break-word;">
                                        <p style="border-top:solid 7px #e20029;font-size:1px;margin:0px auto;width:100%;"></p>
                                    </td>
                                </tr></tbody>
                            </table>
                        </div>
                    </td>
                </tr></tbody>
            </table>
        </div>

        <div style="background:#ffffff;background-color:#ffffff;margin:0px auto;max-width:600px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                <tbody><tr>
                    <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-top:0px;text-align:center;">
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                                <tbody><tr>
                                    <td align="center" style="font-size:0px;padding:10px 25px;padding-top:40px;padding-bottom:0px;word-break:break-word;">
                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                            <tbody><tr>
                                                <td style="width:550px; text-align:center;">
                                                    <img height="auto" style="border:0;display:block;outline:none;text-decoration:none;width:25%;font-size:13px;margin:auto;" 
                                                         width="137.5" 
                                                         src="https://raw.githubusercontent.com/hackharvard/branding/refs/heads/main/static/logoForEmailNoBg.png">
                                                </td>
                                            </tr></tbody>
                                        </table>
                                    </td>
                                </tr></tbody>
                            </table>
                        </div>
                    </td>
                </tr></tbody>
            </table>
        </div>

        <div style="background:#ffffff;background-color:#ffffff;margin:0px auto;max-width:600px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">
                <tbody><tr>
                    <td style="direction:ltr;font-size:0px;padding:20px 0px 20px 0px;padding-bottom:50px;padding-top:20px;text-align:center;">
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                                <tbody>
                                    <tr>
                                        <td align="left" style="font-size:0px;padding:0px 25px 15px 25px;word-break:break-word;">
                                            <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:13px;line-height:1;text-align:left;color:#797e82;">
                                                <h1 style="text-align: center; color: #000000; font-weight: 700; font-size: 34px;">{{action.name}}</h1>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;padding-top:0px;word-break:break-word;">
                                            <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:16px;line-height:22px;text-align:left;color:#000000;">
                                                <p style="margin: 0 0">{{action.description}}</p>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="center" vertical-align="middle" style="font-size:0px;padding:10px 25px;padding-top:20px;word-break:break-word;">
                                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
                                                <tbody><tr>
                                                    <td align="center" role="presentation" valign="middle" bgcolor="#e20029" style="border:none;border-radius:100px;cursor:auto;mso-padding-alt:15px 25px 15px 25px;background:#e20029;">
                                                        <a href="{{action.link}}" target="_blank" style="display:inline-block;background:#e20029;color:#ffffff;font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:14px;font-weight:normal;line-height:120%;margin:0;text-decoration:none;text-transform:none;padding:15px 25px 15px 25px;mso-padding-alt:0px;border-radius:100px;">
                                                            <b style="font-weight: 700"><b style="font-weight: 700">{{action.buttonname}}</b></b>
                                                        </a>
                                                    </td>
                                                </tr></tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;padding-top:0px;word-break:break-word;">
                                            <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:16px;line-height:22px;text-align:left;color:#000000;">
                                                <p style="margin: 30px 0">If you did not request this action, please ignore this email. Additionally, if the above button does not work, you can manually visit <a target="_blank" rel="noopener noreferrer" href="{{action.link}}" style="color: #e20029">{{action.link}}</a>.</p>
                                                <p style="margin: 30px 0">For any questions or concerns, visit our FAQs or reach us at <a target="_blank" rel="noopener noreferrer" href="mailto:team@hackharvard.io" style="color: #e20029">team@hackharvard.io</a>.</p>
                                                <p>With love 🤍,<br>The HackHarvard Team</p>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </td>
                </tr></tbody>
            </table>
        </div>

        <div style="margin:0px auto;max-width:600px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                <tbody><tr>
                    <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                                <tbody><tr>
                                    <td align="center" style="font-size:0px;padding:0px 20px 0px 20px;padding-top:0px;padding-bottom:0px;word-break:break-word;">
                                        <div style="font-family:Open Sans, Helvetica, Arial, sans-serif;font-size:14px;line-height:22px;text-align:center;color:#797e82;">
                                            <p style="margin: 10px 0">
                                                <a target="_blank" rel="noopener noreferrer" href="https://www.hackharvard.io/" style="color: #e20029"><span style="color: #e20029">Main</span></a>
                                                <span style="color: #797e82">&nbsp; &nbsp;|&nbsp; &nbsp;</span>
                                                <a target="_blank" rel="noopener noreferrer" href="{{app.link}}" style="color: #e20029"><span style="color: #e20029">{{app.name}}</span></a>
                                            </p>
                                            <p style="margin: 10px 0">HackHarvard © 2025</p>
                                        </div>
                                    </td>
                                </tr></tbody>
                            </table>
                        </div>
                    </td>
                </tr></tbody>
            </table>
        </div>
    </div>
</body>
</html>"""

    mapping = {
        "{{action.name}}": esc(action_name),
        "{{action.description}}": paragraphize(action_description),
        "{{action.link}}": esc(action_link),
        "{{action.buttonname}}": esc(action_buttonname),
        "{{app.name}}": esc(app_name),
        "{{app.link}}": esc(app_link),
    }
    for needle, replacement in mapping.items():
        tpl = tpl.replace(needle, replacement)

    # Replace logo src
    if logo_url:
        tpl = tpl.replace(
            'src="https://raw.githubusercontent.com/hackharvard/branding/refs/heads/main/static/logoForEmailNoBg.png"',
            f'src="{esc(logo_url)}"'
        )

    # Theme color: swap every hardcoded #e20029 with the chosen one
    if theme_color and theme_color != "#e20029":
        tpl = tpl.replace("#e20029", theme_color)

    # Page background color
    if background_color and background_color != "#f8f8f8":
        tpl = tpl.replace("#f8f8f8", background_color)

    # Footer year (defaults to current year)
    if footer_year is None:
        footer_year = date.today().year
    tpl = re.sub(r"(©\s*)(\d{4})", rf"\1{footer_year}", tpl)

    return tpl