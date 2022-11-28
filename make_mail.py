
def write_mail_header():
    # 이메일 Body
    bodyText = "<style> "
    bodyText = bodyText + "tr.top { " \
                          "height:25px;" \
                          "font-family:Malgun Gothic,굴림,돋움;" \
                          "font-size:14px;" \
                          "color:black;" \
                          "background:white }"
    bodyText = bodyText + "tr.head { " \
                          "height:25px;" \
                          "font-family:Malgun Gothic딕,굴림,돋움;" \
                          "font-size:14px;" \
                          "font-weight:bold;" \
                          "color:white;" \
                          "background:black }"
    bodyText = bodyText + "tr.news { " \
                          "height:25px;" \
                          "font-family:Malgun Gothic,굴림,돋움;" \
                          "font-size:14px;" \
                          "color:white;" \
                          "background:white }"
    bodyText = bodyText + "a { " \
                          "font-family:Malgun Gothic,굴림,돋움;" \
                          "font-size:14px;" \
                          "text-decoration: none;" \
                          "color:black }"
    bodyText = bodyText + "</style>"