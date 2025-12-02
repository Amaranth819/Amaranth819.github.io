from pybtex.database.input import bibtex


def get_personal_data():
    name = ["Xulin", "Chen"]
    email = "xchen168@syr.edu"
    scholar = "https://scholar.google.com/citations?hl=en&user=-RQOxnAAAAAJ"
    github = "Amaranth819"
    linkedin = "xulin-chen-3884b8189"
    cv_link = "https://drive.google.com/file/d/1RIMiF23BMgn9FjcBZ0YaFjGPo_Io9GCs/view?usp=drive_link"
    bio_text = f"""
                <p>
                    Hi, I am a PhD candidate in Computer/Information Science and Engineering (CISE) at <a href="https://ecs.syracuse.edu/academics/electrical-engineering-and-computer-science" target="_blank">Syracuse University</a>, advised by Prof. <a href="https://ecs.syracuse.edu/faculty-staff/garret-ethan-katz" target="_blank">Garrett E. Katz</a>.
                </p>
                <p>
                    <span style="font-weight: bold;">Interests:</span>
                    My current research is centered on Robotics and Reinforcement Learning, but I'm also interested in Neural Network Theory, Generative Models, and Embodied AI.
                </p>
                <p>
                    <span style="font-weight: bold;">Education:</span>
                    I received my Bachelor's degree in Software Engineering in 2018 at <a href="https://www.scut.edu.cn/en/" target="_blank">South China University of Technology</a>, and Master's degree in Computer Science in 2020 at <a href="https://ecs.syracuse.edu/academics/electrical-engineering-and-computer-science" target="_blank">Syracuse University</a>.
                </p>
                <p>
                    <a href="mailto:{email}" style="margin-right: 5px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://www.linkedin.com/in/{linkedin}" target="_blank" style="margin-right: 5px"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                    <a href="{scholar}" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-book"></i> Google Scholar</a>
                    <a href="https://github.com/{github}" target="_blank" style="margin-right: 5px"><i class="fab fa-github fa-lg"></i> Github</a>
                    <a href="{cv_link}" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-file"></i> CV</a>
                    <!-- 
                        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#demo" data-toggle="collapse" style="margin-left: -6px; margin-top: -2px;"><i class="fa-solid fa-trophy"></i>Awards</button> 
                        <div id="demo" class="collapse">
                            <span style="font-weight: bold;">Awards:</span>
                        </div> 
                    -->
                </p>
    """
    footer = """
            <div class="col-sm-12" style="">
                <h4>Homepage Template</h4>
                <p>
                    This page is based on the template of <a href="https://m-niemeyer.github.io/" target="_blank">Michael Niemeyer</a>. Checkout his <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">GitHub repository</a> for instructions on how to use it.<br>
                </p>
            </div>
    """
    return name, bio_text, footer


def get_author_dict():
    return {
        "Sizhe Wei" : "https://sizhewei.github.io/",
        "Fengze Xie" : "https://sites.google.com/view/fengze-xie/home",
        "Garrett E. Katz" : "https://ecs.syracuse.edu/faculty-staff/garret-ethan-katz",
        "Zhenyu Gan" : "https://ecs.syracuse.edu/faculty-staff/zhenyu-gan",
        "Lu Gan" : "https://ganlumomo.github.io/",
        "Ruipeng Liu" : "https://scholar.google.com/citations?user=2Y4HVhgAAAAJ&hl=en",
        "Jiayu Ding" : "https://scholar.google.com/citations?user=YorsCHsAAAAJ&hl=en"
    }


def generate_person_html(
    persons,
    connection=", ",
    make_bold=True,
    make_bold_name="Marcel Hallgarten",
    add_links=True,
    equal_contribution=None,
):
    links = get_author_dict() if add_links else {}
    authors = links.keys()
    s = ""
    self_name = "Xulin Chen"

    equal_contributors = -1
    if equal_contribution is not None:
        equal_contributors = equal_contribution
    for idx, p in enumerate(persons):
        string_part_i = ""
        for name_part_i in p.get_part("first") + p.get_part("last"):
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i

        # if string_part_i in links.keys():
        #     string_part_i = (
        #         f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        #     )
        for author in authors:
            if self_name in string_part_i:
                string_part_i = (
                    f'<b>{string_part_i}</b>'
                )
            if author in string_part_i:
                string_part_i = (
                    f'<a href="{links[author]}" target="_blank">{string_part_i}</a>'
                ) 

        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if idx < equal_contributors:
            string_part_i += "*"
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s


def get_paper_entry(entry_key, entry):
    if "highlight" in entry.fields.keys():
        s = """<div style="background-color: #ffffd0; margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    else:
        s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""

    s += f"""<img src="{entry.fields["img"]}
        " class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    # # Attach a html to the title
    # if "award" in entry.fields.keys():
    #     s += f"""<a href="{entry.fields["html"]}" target="_blank">{entry.fields["title"]}
    #         </a> <span style="color: red;">({entry.fields["award"]})</span><br>"""
    # else:
    #     s += f"""<a href="{entry.fields["html"]}
    #         " target="_blank">{entry.fields["title"]}</a> <br>"""

    # Bold title without a html
    s += f"""<b>{entry.fields["title"]}</b><br>"""

    if "equal_contribution" in entry.fields.keys():
        s += f"""{
            generate_person_html(
                entry.persons["author"],
                equal_contribution=int(entry.fields["equal_contribution"]),
            )
        } <br>"""
    else:
        s += f"""{generate_person_html(entry.persons["author"])} <br>"""

    s += f"""<span style="font-style: italic;">{entry.fields["booktitle"]}</span>, {
        entry.fields["year"]
    } <br>"""

    artefacts = {
        "pdf": "Paper",
        "supp": "Supplementary",
        "video": "Video",
        "poster": "Poster",
        "code": "Project Page",
        "abs": "Abstract",
    }
    i = 0
    for k, v in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += " / "

            # s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            # If k is abstract, then add a button
            if k == 'abs':
                s += f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#demo{entry_key}" data-toggle="collapse" style="margin-left: -14px; margin-top: -4px;">{v}</button> 
                        <div id="demo{entry_key}" class="collapse">
                            {entry.fields[k]}
                        </div>"""
            else:
                s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f"[{entry_key}] Warning: Field {k} missing!")

    cite = "<pre><code>@" + entry.type + "{" + f"{entry_key}, \n"
    cite += (
        "\tauthor = {"
        + f"{
            generate_person_html(
                entry.persons['author'],
                make_bold=False,
                add_links=False,
                connection=' and ',
            )
        }"
        + "}, \n"
    )
    for entr in ["title", "booktitle", "year"]:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    # # Add a button for showing the bibtex entry
    # s += (
    #     " /"
    #     + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{
    #         entry_key
    #     }" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Bibtex</button><div class="collapse" id="collapse{
    #         entry_key
    #     }"><div class="card card-body">{cite}</div></div>"""
    # )
    s += """ </div> </div> </div>"""
    return s


def get_teaching_entry(entry_key, entry):
    imgs = {
        "proseminar": "assets/img/teaching/academia.svg",
        "seminar": "assets/img/teaching/seminar.svg",
        "lecture": "assets/img/teaching/lecture.svg",
    }
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-1">"""
    s += f"""<img src="{imgs[entry.fields["type"].lower()]}
                                                        " class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-11">"""

    artefacts = ["year", "type", "course", "institution", "desc"]
    assert all(
        [k in entry.fields.keys() for k in artefacts]
    ), f"Teaching entry must contain {artefacts}, but got {entry.fields.keys()}"
    s += f"""{entry.fields["type"]}: <span style="font-weight: bold;">{
        entry.fields["course"]
    }</span><br>"""
    s += f"""<span style="font-style: italic;">{entry.fields["institution"]}</span>, {
        entry.fields["year"]
    }<br>"""

    course_id = (
        entry.fields["course"].replace(" ", "_").lower() + "_" + entry.fields["year"]
    )
    s += f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#{
        course_id
    }" data-toggle="collapse" style="margin-left: -6px; margin-top: -2px;"><i class="fa-regular fa-file-lines"></i> Description</button>"""
    s += f"""<div id="{course_id}" class="collapse">
        {entry.fields["desc"]}
    </div>"""

    s += """ </div> </div> </div>"""
    return s


def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields["img"]}
        " class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields["title"]}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields["booktitle"]}</span>, {
        entry.fields["year"]
    } <br>"""

    artefacts = {"slides": "Slides", "video": "Recording"}
    i = 0
    for k, v in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += " / "
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f"[{entry_key}] Warning: Field {k} missing!")
    s += """ </div> </div> </div>"""
    return s


def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file("publication_list.bib")
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_paper_entry(k, bib_data.entries[k])
    return s


def get_teaching_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file("teaching_list.bib")
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_teaching_entry(k, bib_data.entries[k])
    return s


def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file("talk_list.bib")
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_talk_entry(k, bib_data.entries[k])
    return s


# Edit services here
def get_service_html():
    services = [
        ("Reviewer", "ICRA (2026), IROS (2024)"),
        ("Graduate Teaching Assistant", "MIT Beaver Works Summer Institute (Orange Works), 2025"),
        ("Graduate Teaching Assistant", "TACNY Summer STEM Trekker Program, 2022 and 2023"),
    ] # title, content

    s = ""
    s += "<ul>"
    for key, content in services:
        s += f"<li><b>{key}</b>: {content}.</li>"
    s += "</ul>"
    return s


def get_index_html():
    pub = get_publications_html()
    talks = get_talks_html()
    teaching = get_teaching_html()
    name, bio_text, footer = get_personal_data()
    services = get_service_html()

    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer">
  <title>{name[0] + " " + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.png">
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="margin-bottom: 1em;">
                    <!-- <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3> -->
                    <h3 class="display-4" style="text-align: center;">{name[0]} {name[1]}</h3>
                    </div>
                    <br>
                    <div class="col-md-8" style="">
                        {bio_text}
                    </div>
                    <div class="col-md-4" style="">
                        <img src="assets/img/profile.png" class="img-thumbnail mx-auto d-block" width="200px" alt="Profile picture">
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Selected Papers</h4>
                        {pub}
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Services</h4>
                        {services}
                    </div>
                </div>
                <!-- <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Teaching</h4>
                        {teaching}
                    </div>
                </div> -->
                <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
                    {footer}
                </div>
            </div>
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename="index.html"):
    s = get_index_html()
    with open(filename, "w") as f:
        f.write(s)
    print(f"Written index content to {filename}.")


if __name__ == "__main__":
    write_index_html("index.html")
