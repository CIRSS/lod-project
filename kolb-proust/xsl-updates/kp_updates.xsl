            <div id="tooltip">
               <div id="tooltip_title"></div>
               <div id="tooltip_content">
                  <div id="tooltip_lifespan"></div>

                  <label for="tooltip_gender">Gender: </label><span id="tooltip_gender"></span>
                  <div id="tooltip_links">
                     <div id="tooltip_dynamic_links"></div>
                     <a id="local_link">More From Proust Collection</a>
                  </div>
               </div>
            </div>
<!--            <xsl:element name="div">
               <xsl:attribute name="id">tooltip</xsl:attribute>
            </xsl:element>-->

            <script language="javascript" defer="true">
               <![CDATA[
                  $(".name").mouseover(function(event) {
                     event.preventDefault();
                     $("#tooltip").css("visibility","visible");
                     $("#tooltip_dynamic_links").html("");
                     $.get("http://kolbproust.library.illinois.edu/xmlSparql/getName.asp?" + event.target.href.substring('http://kolbproust.library.illinois.edu/proust/search?subject='.length), function(data) {
                        $("#tooltip_title").text(data['name']);
                        $("#local_link").attr("href",event.target.href);

                        if ('birthDate' in data || 'deathDate' in data) {
                           let lifespan = "";
                           if ('birthDate' in data) {
                              lifespan += data['birthDate']['value'];
                           }
                           lifespan += '-';
                           if ('deathDate' in data) {
                              lifespan += data['deathDate']['value'];
                           }
                           $("#tooltip_lifespan").text(lifespan);
                        }
                        else {
                           $("#tooltip_lifespan").text("");
                        }

                        if ('gender' in data) {
                           $("label[for=tooltip_gender]").css("display","inline");
                           $("#tooltip_gender").text(data['gender']);
                        }
                        else {
                           $("label[for=tooltip_gender]").css("display","none");
                           $("#tooltip_gender").text("");
                        }

                        if ('sameAs' in data) {
                           if(data.sameAs.length !== undefined) {
                              data.sameAs.forEach(function(element) {
                                 let a = document.createElement('a');
                                 let linkText = ""
                                 if (element['id'].indexOf('fr.wikipedia') != -1) {
                                    linkText = document.createTextNode("French Wikipedia");
                                 }
                                 else if (element['id'].indexOf('en.wikipedia') != -1) {
                                    linkText = document.createTextNode("English Wikipedia");
                                 }
                                 else if (element['id'].indexOf('viaf') != -1) {
                                    linkText = document.createTextNode("VIAF");
                                 }
                                 else {
                                    linkText = document.createTextNode("Other Link");
                                 }
                                 
                                 a.appendChild(linkText);
                                 a.href = element['id'];
                                 $("#tooltip_dynamic_links").prepend(a);
                                 a.append(document.createElement("br"));
                              });
                           }
                           else {
                              let a = document.createElement('a');
                              let linkText = ""
                              if (data['sameAs']["id"].indexOf('fr.wikipedia') != -1) {
                                 linkText = document.createTextNode("French Wikipedia");
                              }
                              else if (data['sameAs']["id"].indexOf('en.wikipedia') != -1) {
                                 linkText = document.createTextNode("English Wikipedia");
                              }
                              else if (data['sameAs']["id"].indexOf('viaf') != -1) {
                                 linkText = document.createTextNode("VIAF");
                              }
                              else {
                                 linkText = document.createTextNode("Other Link");
                              }
                              
                              a.appendChild(linkText);
                              a.href = data["sameAs"]["id"];
                              $("#tooltip_dynamic_links").prepend(a);
                              a.append(document.createElement("br"));
                           }
                        }

                        if ($(event.target).height() != $(".date").height()) {
                           let midpoint = 42 + $(".widthResult").width() + $(".facet").width() + 21.5 + ($(".date").width()/2);
                           if (Math.sign(event.pageX - midpoint) == -1) {
                              $("#tooltip").css("left",$(event.target).offset().left - $("#tooltip").width()/2 - 8);
                              $("#tooltip").css("top",$(event.target).offset().top - $("#tooltip").height());
                           }
                           else {
                              $("#tooltip").css("left",$(event.target).offset().left + $(event.target).width() - $("#tooltip").width()/2 - 8);
                              $("#tooltip").css("top",$(event.target).offset().top - $(".date").height() - $("#tooltip").height());
                           }
                        }
                        else {
                           $("#tooltip").css("left",$(event.target).offset().left + ($(event.target).width()/2) - $("#tooltip").width()/2 - 8);
                           $("#tooltip").css("top",$(event.target).offset().top - $(event.target).height() - $("#tooltip").height());
                        }
                     })
                  });

                  $("#tooltip").mouseleave(function(event) {
                     $("#tooltip").css("visibility","hidden");
					 $("#tooltip_title").text("");
                  });

                  $(document).keyup(function(e) {
                     if (e.keyCode === 27) {
                        $("#tooltip").css("visibility","hidden");
                     }
                  });
               ]]>
            </script>