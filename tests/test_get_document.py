def test_get_document(client):
    rv = client.get('/docs/courses/csi2132')
    # Check if course code is in the result
    assert b"csi2132" in rv.data
    # Check if course title is in the result
    assert b"CSI 2132 Databases I" in rv.data
    # Check if description is in the result
    assert b"Fundamental database concepts. " \
           b"Entity-Relationship modeling. Relational algebra and relational calculus. " \
           b"Relational databases. Database definition and manipulation using SQL. " \
           b"Embedded SQL. Functional dependencies and normalization. " \
           b"Introduction to physical database design. " \
           b"Design and implementation of a database application in a team project." \
           b"Course Component: Laboratory, Lecture, " \
           b"TutorialPrerequisite: CSI 2110." in rv.data
